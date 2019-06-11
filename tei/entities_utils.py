import lxml.etree as ET


def org_to_tei(res):
    org = ET.Element("{http://www.tei-c.org/ns/1.0}org")
    org.attrib['{http://www.w3.org/XML/1998/namespace}id'] = "org__{}".format(
        res.id
    )
    orgName = ET.Element("{http://www.tei-c.org/ns/1.0}orgName")
    orgName.text = res.written_name
    org.append(orgName)

    return org


def person_to_tei(res):
    person = ET.Element("{http://www.tei-c.org/ns/1.0}person")
    person.attrib['{http://www.w3.org/XML/1998/namespace}id'] = "person__{}".format(
        res.id
    )
    persName = ET.Element("{http://www.tei-c.org/ns/1.0}persName")
    if res.name is not None:
        surname = ET.Element("{http://www.tei-c.org/ns/1.0}surname")
        surname.text = getattr(res, 'name', 'N.')
        persName.append(surname)
    else:
        persName.text = res.written_name
    if res.forename is not None:
        forename = ET.Element("{http://www.tei-c.org/ns/1.0}forename")
        forename.text = getattr(res, 'forename', 'N.')
        persName.append(forename)

    if res.acad_title is not None:
        acad_title = ET.Element("{http://www.tei-c.org/ns/1.0}roleName")
        acad_title.text = getattr(res, 'acad_title', 'N.')
        persName.append(acad_title)
    person.append(persName)

    if res.date_of_birth is not None:
        birth = ET.Element("{http://www.tei-c.org/ns/1.0}birth")
        birth.attrib['when'] = f"{res.date_of_birth}"
        birth.text = f"{res.date_of_birth}"
    elif res.date_of_birth_written is not None:
        birth = ET.Element("{http://www.tei-c.org/ns/1.0}birth")
        birth.text = res.date_of_birth_written
    else:
        birth = ET.Element("{http://www.tei-c.org/ns/1.0}birth")
        birth.text = "kein Geburtsdatum angeführt"

    if res.place_of_birth is not None:
        birth_place = ET.Element("{http://www.tei-c.org/ns/1.0}placeName")
        birth_place.attrib['key'] = f"#place__{res.place_of_birth.id}"
        birth_place.text = res.place_of_birth.name
        birth.append(birth_place)
    person.append(birth)

    if res.date_of_death is not None:
        death = ET.Element("{http://www.tei-c.org/ns/1.0}death")
        death.attrib['when'] = f"{res.date_of_death}"
        death.text = f"{res.date_of_death}"
    elif res.date_of_death_written is not None:
        death = ET.Element("{http://www.tei-c.org/ns/1.0}death")
        death.text = res.date_of_death_written
    else:
        death = ET.Element("{http://www.tei-c.org/ns/1.0}death")
        death.text = "kein Geburtsdatum angeführt"

    if res.place_of_death is not None:
        death_place = ET.Element("{http://www.tei-c.org/ns/1.0}placeName")
        death_place.attrib['key'] = f"#place__{res.place_of_death.id}"
        death_place.text = res.place_of_death.name
        death.append(death_place)
    person.append(death)

    if res.authority_url is not None and res.authority_url != "":
        idno = ET.Element("{http://www.tei-c.org/ns/1.0}idno")
        idno.text = res.authority_url
        person.append(idno)
    return person
