import pickle
import os
import re


from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db.models.query import QuerySet

from rdflib import Graph, Namespace, URIRef, Literal, XSD
from rdflib.namespace import RDF

from browsing.browsing_utils import model_to_dict
from webpage.metadata import PROJECT_METADATA

ARCHE_CONST_MAPPINGS = getattr(settings, 'ARCHE_CONST_MAPPINGS', False)

ARCHE_LANG = getattr(settings, 'ARCHE_LANG', 'en')
ARCHE_BASE_URL = getattr(settings, 'ARCHE_BASE_URL', 'https://id.acdh.oeaw.ac.at/MYPROJECT')


repo_schema = "https://raw.githubusercontent.com/acdh-oeaw/repo-schema/master/acdh-schema.owl"
acdh_ns = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
owl_ns = Namespace("http://www.w3.org/2002/07/owl#")
rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")


def get_prop_types(repo_schema_url=repo_schema):
    g = Graph()
    g.parse(repo_schema, format='xml')
    prop_types = {}
    for s in g.subjects(RDF.type, None):
        if s.startswith('https://vocabs.acdh'):
            prop_name = s.split('#')[-1]
            for range_prop in g.objects(s, rdfs_ns.range):
                prop_types[prop_name] = range_prop.split('#')[-1]
    return prop_types


ARCHE_PROPS_LOOKUP = get_prop_types()

DESCRIPTION = """„Die große Transformation“ versammelt relevante Quellen aus unterschiedlichen Archiven zu Fragen der Reform der Bundes- und Wiener Gemeindeverwaltung in der unmittelbaren Nachkriegszeit 1918 bis 1920. Der in dieser Datensammlung edierte Quellenkorpus umfasst folgende Bestände:
* Verhandlungsschriften (Komitee Staatsangestellte)
* Enquete (Zielrichtung mehr Mitbestimmung, Personalvertretung)
* Relevante Akten Staatsrat und Kabinettsrat
* Relevante Gesetze (Staatsgesetzblatt)
* Zeitungen, Zeitschriften
* Akten der Allgemeinen Registratur der Magistratsdirektion, Wiener Stadt- und Landesarchiv
* Gemeinderats- und Stadtratsprotokolle wie in den Amtsblättern der Stadt Wien veröffentlicht
* Akten des Parteiarchivs vor 1934 der SDAP, Verein der Geschichte der Arbeiterbewegung in Wien (VGA)
* Tagblattarchiv zum Stichwort Beamte, Wienbibliothek
* ÖGB-Archiv, Material zu Beamtenorganisationen
„Die große Transformation“ erlaubt erstmals einen Blick in komparativer Perspektive auf die Zusammenhänge in der Transformation der beiden Verwaltungsebenen durch die Republiksgründung. Die aus den Quellen erstellten Datensätze wurden beschlagwortet und die in ihnen erwähnten Personen, Institutionen und Orte erfasst."""

vhelfert = URIRef("https://id.acdh.oeaw.ac.at/vhelfert")
kmegner = URIRef("https://id.acdh.oeaw.ac.at/kmegner")
gsteiner = URIRef("https://id.acdh.oeaw.ac.at/gsteiner")
tgarstenauer = URIRef("https://id.acdh.oeaw.ac.at/tgarstenauer")
pbecker = URIRef("https://id.acdh.oeaw.ac.at/pbecker")
tstockinger = URIRef("https://id.acdh.oeaw.ac.at/tstockinger")
pandorfer = URIRef('https://d-nb.info/gnd/1043833846')
univie = URIRef('https://d-nb.info/gnd/2024703-5')
publication = URIRef("https://d-nb.info/1207562777")


def serialize_project():
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}")
    g.add((sub, RDF.type, acdh_ns.TopCollection))
    g.add(
        (
            sub,
            acdh_ns.hasPid,
            Literal(
                'https://hdl.handle.net/21.11115/0000-000E-558C-5',
                datatype=XSD.URIRef
            )
        )
    )
    g.add(
        (sub, acdh_ns.hasCoverageStartDate, Literal('1918-01-01', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasCoverageEndDate, Literal('1920-12-31', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasCreatedStartDate, Literal('2018-01-01', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasCreatedEndDate, Literal('2019-12-31', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasSpatialCoverage, URIRef('https://www.geonames.org/2761367'))
    )
    g.add(
        (sub, acdh_ns.hasTitle, Literal("Die Große Transformation", lang='de'))
    )
    g.add(
        (publication, RDF.type, acdh_ns.Publication)
    )
    g.add(
        (
            publication, acdh_ns.hasTitle, Literal(
                "Hofratsdämmerung? : Verwaltung und ihr Personal in den Nachfolgestaaten der Habsburgermonarchie 1918 bis 1920",
                lang="de"
            )
        )
    )
    g.add(
        (publication, acdh_ns.isDerivedPublication, sub)
    )
    # define persons
    g.add(
        (vhelfert, acdh_ns.hasTitle, Literal("Veronika Helfert", lang='und'))
    )
    g.add(
        (vhelfert, acdh_ns.hasFirstName, Literal("Veronika", lang="und"))
    )
    g.add(
        (vhelfert, acdh_ns.hasLastName, Literal("Helfert", lang="und"))
    )
    g.add(
        (vhelfert, acdh_ns.hasIdentifier, URIRef("https://d-nb.info/gnd/1080815546"))
    )
    g.add((vhelfert, RDF.type, acdh_ns.Person))
    g.add(
        (kmegner, acdh_ns.hasTitle, Literal("Karl Megner", lang="und"))
    )
    g.add(
        (kmegner, acdh_ns.hasFirstName, Literal("Karl", lang="und"))
    )
    g.add(
        (kmegner, acdh_ns.hasLastName, Literal("Megner", lang="und"))
    )
    g.add(
        (kmegner, acdh_ns.hasIdentifier, URIRef("https://d-nb.info/gnd/170333639"))
    )
    g.add((kmegner, RDF.type, acdh_ns.Person))
    g.add(
        (gsteiner, acdh_ns.hasTitle, Literal("Guenther Steiner", lang="und"))
    )
    g.add(
        (gsteiner, acdh_ns.hasFirstName, Literal("Guenther", lang="und"))
    )
    g.add(
        (gsteiner, acdh_ns.hasLastName, Literal("Steiner", lang="und"))
    )
    g.add((gsteiner, RDF.type, acdh_ns.Person))
    g.add(
        (tgarstenauer, acdh_ns.hasTitle, Literal("Theresa Garstenauer", lang='und'))
    )
    g.add(
        (tgarstenauer, acdh_ns.hasFirstName, Literal("Theresa", lang="und"))
    )
    g.add(
        (tgarstenauer, acdh_ns.hasLastName, Literal("Garstenauer", lang="und"))
    )
    g.add(
        (tgarstenauer, acdh_ns.hasIdentifier, URIRef("https://d-nb.info/gnd/141560282"))
    )
    g.add(
        (pbecker, acdh_ns.hasTitle, Literal("Peter Becker", lang='und'))
    )
    g.add(
        (pbecker, acdh_ns.hasFirstName, Literal("Peter", lang="und"))
    )
    g.add(
        (pbecker, acdh_ns.hasLastName, Literal("Becker", lang="und"))
    )
    g.add(
        (pbecker, acdh_ns.hasIdentifier, URIRef("https://d-nb.info/gnd/131500481"))
    )
    g.add(
        (tstockinger, acdh_ns.hasTitle, Literal("Thomas Stockinger", lang='und'))
    )
    g.add(
        (tstockinger, acdh_ns.hasFirstName, Literal("Thomas", lang="und"))
    )
    g.add(
        (tstockinger, acdh_ns.hasLastName, Literal("Stockinger", lang="und"))
    )
    g.add(
        (tstockinger, acdh_ns.hasIdentifier, URIRef("https://d-nb.info/gnd/1210952947"))
    )
    g.add(
        (pandorfer, acdh_ns.hasTitle, Literal("Peter Andorfer", lang='und'))
    )
    g.add((univie, RDF.type, acdh_ns.Organisation))
    g.add(
        (univie, acdh_ns.hasTitle, Literal("Universität Wien", lang='und'))
    )

    g.add(
        (
            sub,
            acdh_ns.hasDescription,
            Literal(DESCRIPTION, lang=ARCHE_LANG))
    )
    g.add(
        (sub, acdh_ns.hasCreator, vhelfert)
    )
    g.add(
        (sub, acdh_ns.hasCreator, kmegner)
    )
    g.add(
        (sub, acdh_ns.hasCreator, gsteiner)
    )
    g.add(
        (sub, acdh_ns.hasCreator, tgarstenauer)
    )
    g.add(
        (sub, acdh_ns.hasPrincipalInvestigator, pbecker)
    )
    g.add(
        (sub, acdh_ns.hasContributor, tstockinger)
    )
    g.add(
        (sub, acdh_ns.hasContributor, pandorfer)
    )
    g.add(
        (sub, acdh_ns.hasCurator, pandorfer)
    )
    g.add(
        (sub, acdh_ns.hasLanguage, URIRef('https://vocabs.acdh.oeaw.ac.at/iso6393/deu'))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == 'string':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
    return g


def get_arche_id(res, id_prop="pk", arche_uri=ARCHE_BASE_URL):
    """ function to generate generic ARCHE-IDs
        :param res: A model object
        :param id_prop: The object's primary key property
        :param arche_uri: A base url; should be configued in the projects settings file
        :return: An ARCHE-ID (URI)
    """
    if isinstance(res, str):
        return res
    else:
        app_name = res.__class__._meta.app_label.lower()
        class_name = res.__class__.__name__.lower()
        return "/".join(
            [arche_uri, app_name, class_name, f"{getattr(res, id_prop)}"]
        )


def as_arche_graph(res):
    g = Graph()
    sub = URIRef(get_arche_id(res))
    g.add(
        (sub, acdh_ns.hasTitle, Literal(
            f"{res.__str__().replace('Titel: ', '')}",
            lang=ARCHE_LANG)
        )
    )
    if 'http' in res.pid:
        g.add(
            (sub, acdh_ns.hasPid, Literal(res.pid, datatype=XSD.URIRef))
        )
    g.add((sub, RDF.type, acdh_ns.Resource))
    if res.signature:
        g.add(
            (
                sub,
                acdh_ns.hasNonLinkedIdentifier,
                Literal(f"{res.signature}")
            )
        )
    col = Graph()
    col_sub = URIRef(f"{ARCHE_BASE_URL}")
    g.add(
        (
            sub,
            acdh_ns.hasDescription,
            Literal(
                f"{res.abstract}",
                lang='de'
            )
        )
    )
    g.add(
        (sub, acdh_ns.isPartOf, col_sub)
    )
    g.add(
        (sub, acdh_ns.hasCustomXsl, Literal('https://tei4arche.acdh-dev.oeaw.ac.at/xsl/gtrans.xsl'))
    )
    g.add(
        (sub, acdh_ns.hasSchema, Literal('https://tei-c.org/Vault/P5/4.2.2/xml/tei/custom/schema/relaxng/tei_all.rng'))
    )
    g.add(
        (sub, acdh_ns.hasLanguage, URIRef('https://vocabs.acdh.oeaw.ac.at/iso6393/deu'))
    )
    if res.not_before is not None:
        g.add(
            (sub, acdh_ns.hasCoverageStartDate, Literal(res.not_before, datatype=XSD.date))
        )
    if res.permalink is not None:
        g.add(
            (sub, acdh_ns.hasUrl, Literal(res.permalink, datatype=XSD.URIRef))
        )
    if res.not_after is not None:
        g.add(
            (sub, acdh_ns.hasCoverageEndDate, Literal(res.not_after, datatype=XSD.date))
        )
    elif res.not_before is not None:
        g.add(
            (sub, acdh_ns.hasCoverageEndDate, Literal(res.not_before, datatype=XSD.date))
        )
    
    for x in res.mentioned_place.all():
        pl = Graph()
        pl_uri = URIRef(x.arche_id())
        pl.add(
            (pl_uri, RDF.type, acdh_ns.Place)
        )
        pl.add(
            (pl_uri, acdh_ns.hasTitle, Literal(f"{x}", lang="und"))
        )
        g.add(
            (sub, acdh_ns.hasSpatialCoverage, pl_uri)
        )
        g = g + pl
    for x in res.subject_norm.all():
        g.add(
            (sub, acdh_ns.hasSubject, Literal(x.pref_label, lang="de"))
        )
    for x in res.creators.all():
        p = Graph()
        p_uri = URIRef(f"https://id.acdh.oeaw.ac.at/{x.username}")
        g.add(
            (sub, acdh_ns.hasCreator, p_uri)
        )
    for x in res.mentioned_inst.all() | res.creator_inst.all():
        p = Graph()
        p_uri = URIRef(get_arche_id(x))
        p.add(
            (p_uri, RDF.type, acdh_ns.Organisation)
        )
        p.add(
            (
                p_uri, acdh_ns.hasTitle, Literal(
                    f"{x.written_name}",
                    lang="de"
                )
            )
        )
        g.add(
            (sub, acdh_ns.hasActor, p_uri)
        )
        if x.comment:
            p.add(
                (p_uri, acdh_ns.hasDescription, Literal(f"{x.comment}", lang="de"))
            )
        g = g + p
    for x in res.mentioned_person.all() | res.creator_person.all():
        p = Graph()
        p_uri = URIRef(x.arche_id())
        if "d-nb.info/gnd/" in x.authority_url:
            pass
        elif x.authority_url.startswith('http'):
            p.add(
                (p_uri, acdh_ns.hasUrl, Literal(f"{x.authority_url}", datatype=XSD.URIRef))
            )
        p.add(
            (p_uri, RDF.type, acdh_ns.Person)
        )
        p.add(
            (p_uri, acdh_ns.hasTitle, Literal(f"{x}", lang="de"))
        )
        if x.forename:
            p.add(
                (p_uri, acdh_ns.hasFirstName, Literal(f"{x.forename}", lang="und"))
            )
        if x.name:
            p.add(
                (p_uri, acdh_ns.hasLastName, Literal(f"{x.name}", lang="und"))
            )
        if x.acad_title:
            p.add(
                (p_uri, acdh_ns.hasPersonalTitle, Literal(f"{x.acad_title}"))
            )
        if x.biography:
            p.add(
                (p_uri, acdh_ns.hasDescription, Literal(f"{x.biography}", lang="de"))
            )
        g.add(
            (sub, acdh_ns.hasActor, p_uri)
        )
        g = g + p
    g.add(
        (
            sub,
            acdh_ns.hasCategory,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei"))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == 'string':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
    g = g + col
    return g
