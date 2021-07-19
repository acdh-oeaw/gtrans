import datetime
import lxml.etree as ET

from tei.partials import TEI_NSMAP, custom_escape
from webpage.metadata import PROJECT_METADATA

from reversion.models import Version


class MakeTeiDoc():
    def __init__(self, res, PROJECT_METADATA=PROJECT_METADATA):
        self.nsmap = TEI_NSMAP
        self.project_md = PROJECT_METADATA
        self.base = "https://id.acdh.oeaw.ac.at/gtrans/archiv/archresource/"
        self.res = res
        if self.res.get_prev():
            self.prev = f'prev="{self.base}{self.res.get_prev_id()}"'
        else: 
            self.prev = ""
        if self.res.get_next():
            self.next = f'next="{self.base}{self.res.get_next_id()}"'
        else: 
            self.next = ""  
        self.res_url = f"{self.base}{self.res.get_absolute_url()}"
        self.creators = " ".join(["#{}".format(x.username) for x in self.res.creators.all()])
        self.written_date = self.res.written_date
        if self.res.abstract != "":
            self.abstract = f"{self.res.abstract}"
        else:
            self.abstract = None

        if self.abstract is not None:
            self.abstract = custom_escape(self.abstract)

    def make_editors(self):
        ed_pers = self.res.creators.all()
        if ed_pers.count() > 0:
            editors = []
            for x in ed_pers:
                root_el = ET.Element("{http://www.tei-c.org/ns/1.0}editor")
                rs = ET.Element("{http://www.tei-c.org/ns/1.0}rs")
                rs.attrib['ref'] = f"#{x.username}"
                rs.text = f"{x.last_name}, {x.first_name}"
                root_el.append(rs)
                editors.append(root_el)
            return editors
        else:
            return []

    def not_before(self):
        if self.res.not_before is not None:
            return self.res.not_before
        else:
            return datetime.date(1918, 1, 1)

    def not_after(self):
        if self.res.not_after is not None:
            return self.res.not_after
        elif self.not_before is not None:
            return self.not_before()
        else:
            return datetime.date(1920, 12, 31)

    def populate_header(self):
        res_url = f"https://gtrans.acdh.oeaw.ac.at{self.res.get_absolute_url()}"
        creators = " ".join(["#{}".format(x.username) for x in self.res.creators.all()])
        header = f"""
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="archesource-{self.res.id}" {self.prev} {self.next} xml:base="{self.base}">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title type="main">{self.res.title}</title>
            <title type="sub">{self.project_md['title']}</title>
         </titleStmt>
         <publicationStmt>
            <publisher>Austrian Centre for Digital Humanities</publisher>
            <idno type="django_id">{res_url}</idno>
         </publicationStmt>
         <sourceDesc>
            <msDesc>
               <msIdentifier>
                    <repository>{self.res.archiv}</repository>
                    <msName>{self.res.signature}</msName>
               </msIdentifier>
               <msContents>
               </msContents>
               <physDesc>
                    <typeDesc>
                        <p>{self.res.res_type}</p>
                    </typeDesc>
               </physDesc>
            </msDesc>
         </sourceDesc>
      </fileDesc>
     <profileDesc>
        <abstract resp="{creators}">
            <p>{self.abstract}</p>
        </abstract>
        <creation>
            <date notBefore="{self.not_before()}" notAfter="{self.not_after()}">
                {self.written_date}
            </date>
        </creation>
     </profileDesc>
  </teiHeader>
  <text>
      <body>
         <p></p>
      </body>
      <back>
         <listPerson>
            <head>Erwähnte Personen</head>
            <person/>
         </listPerson>
         <listPlace>
            <head>Erwähnte Orte</head>
            <place/>
         </listPlace>
         <listOrg>
            <head>Erwähnte Institutionen</head>
            <org/>
         </listOrg>
      </back>
  </text>
</TEI>
"""
        return header

    def create_header_node(self):
        header = ET.fromstring(self.populate_header())
        return header

    def pop_mentions(self):
        cur_doc = self.create_header_node()

        list_person = cur_doc.xpath(".//tei:listPerson", namespaces=self.nsmap)[0]
        for x in self.res.mentioned_person.all():
            list_person.append(x.as_tei_node())

        list_org = cur_doc.xpath(".//tei:listOrg", namespaces=self.nsmap)[0]
        for x in self.res.mentioned_inst.all():
            list_org.append(x.as_tei_node())

        list_place = cur_doc.xpath(".//tei:listPlace", namespaces=self.nsmap)[0]
        for x in self.res.mentioned_place.all():
            list_place.append(x.as_tei_node())

        if len(self.make_editors()) > 0:
            title_stmt = cur_doc.xpath(".//tei:titleStmt", namespaces=self.nsmap)[0]
            for x in self.make_editors():
                title_stmt.append(x)

        if self.res.permalink != None:
            permalink = cur_doc.xpath(".//tei:msIdentifier", namespaces=self.nsmap)[0]
            idno = ET.Element("{http://www.tei-c.org/ns/1.0}idno")
            idno.text = self.res.permalink
            permalink.append(idno)

        if self.res.notes != None:
            notes = cur_doc.xpath(".//tei:msContents", namespaces=self.nsmap)[0]
            p = ET.Element("{http://www.tei-c.org/ns/1.0}p")
            p.text = self.res.notes
            notes.append(p)

        if self.res.creator_person != None:
            creator = cur_doc.xpath(".//tei:msContents", namespaces=self.nsmap)[0]
            for x in self.res.creator_person.all():
                msItem = ET.Element("{http://www.tei-c.org/ns/1.0}msItem")
                author = ET.Element("{http://www.tei-c.org/ns/1.0}author")
                author.text = x.acad_title + ' ' + x.forename + ' ' + x.name
                msItem.append(author)
                creator.append(msItem)

        if self.res.creator_inst != None:
            creator = cur_doc.xpath(".//tei:msContents", namespaces=self.nsmap)[0]
            for x in self.res.creator_inst.all():
                msItem = ET.Element("{http://www.tei-c.org/ns/1.0}msItem")
                author = ET.Element("{http://www.tei-c.org/ns/1.0}author")
                author.text = x.written_name
                msItem.append(author)
                creator.append(msItem)

        if self.res.subject_free != None or self.res.subject_norm != None:
            profileDesc = cur_doc.xpath(".//tei:profileDesc", namespaces=self.nsmap)[0]
            textClass = ET.Element("{http://www.tei-c.org/ns/1.0}textClass")
            profileDesc.append(textClass)

        if self.res.subject_free != None:
            textClass = cur_doc.xpath(".//tei:textClass", namespaces=self.nsmap)[0]
            keywords = ET.Element("{http://www.tei-c.org/ns/1.0}keywords")
            keywords.text = self.res.subject_free
            keywords.attrib["scheme"] = "original"
            textClass.append(keywords)

        if self.res.subject_norm != None:
            textClass = cur_doc.xpath(".//tei:textClass", namespaces=self.nsmap)[0]
            for x in self.res.subject_norm.all():                
                keywords = ET.Element("{http://www.tei-c.org/ns/1.0}keywords")
                keywords.text = x.pref_label     
                keywords.attrib["scheme"] = "http://www.w3.org/2004/02/skos/core#prefLabel"
                textClass.append(keywords)

        # context = Version.objects.get_for_object(self.res)
        # if context:
        #     teiHeader = cur_doc.xpath(".//tei:teiHeader", namespaces=self.nsmap)[0]
        #     revisionDesc = ET.Element("{http://www.tei-c.org/ns/1.0}revisionDesc")
        #     for x in context.all():
        #         change = ET.Element("{http://www.tei-c.org/ns/1.0}change")
        #         change.attrib["when"] = x.revision.date_created
        #         change.text = x.revision.user
        #         revisionDesc.append(change)
        #     teiHeader.append(revisionDesc)
        return cur_doc

    def export_full_doc(self):
        return self.pop_mentions()

    def export_full_doc_str(self, file="temp.xml"):
        with open(file, 'wb') as f:
            f.write(ET.tostring(self.pop_mentions(), pretty_print=True, encoding='UTF-8'))
        return file
