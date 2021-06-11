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


def serialize_project():
    g = Graph()
    sub = URIRef(f"{ARCHE_BASE_URL}")
    g.add((sub, RDF.type, acdh_ns.TopCollection))
    g.add(
        (sub, acdh_ns.hasCoverageStartDate, Literal('1918-01-01', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasCoverageEndDate, Literal('1920-12-31', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasTitle, Literal(f"{PROJECT_METADATA['title']}", lang='en'))
    )
    # define persons
    vhelfert = URIRef("https://id.acdh.oeaw.ac.at/vhelfert")
    kmegner = URIRef("https://id.acdh.oeaw.ac.at/kmegner")
    gsteiner = URIRef("https://id.acdh.oeaw.ac.at/gsteiner")
    tgarstenauer = URIRef("https://id.acdh.oeaw.ac.at/tgarstenauer")
    pbecker = URIRef("https://id.acdh.oeaw.ac.at/pbecker")
    tstockinger = URIRef("https://id.acdh.oeaw.ac.at/tstockinger")
    pandorfer = URIRef('https://d-nb.info/gnd/1043833846')
    univie = URIRef('https://d-nb.info/gnd/2024703-5')
    g.add(
        (vhelfert, acdh_ns.hasTitle, Literal("Veronika Helfert", lang='de'))
    )
    g.add(
        (vhelfert, acdh_ns.hasFirstName, Literal("Veronika", lang="de"))
    )
    g.add(
        (vhelfert, acdh_ns.hasLastName, Literal("Helfert", lang="de"))
    )
    g.add((vhelfert, RDF.type, acdh_ns.Person))
    g.add(
        (kmegner, acdh_ns.hasTitle, Literal("Karl Megner", lang="de"))
    )
    g.add(
        (kmegner, acdh_ns.hasFirstName, Literal("Karl", lang="de"))
    )
    g.add(
        (kmegner, acdh_ns.hasLastName, Literal("Megner", lang="de"))
    )
    g.add((kmegner, RDF.type, acdh_ns.Person))
    g.add(
        (gsteiner, acdh_ns.hasTitle, Literal("Guenther Steiner", lang="de"))
    )
    g.add(
        (gsteiner, acdh_ns.hasFirstName, Literal("Guenther", lang="de"))
    )
    g.add(
        (gsteiner, acdh_ns.hasLastName, Literal("Steiner", lang="de"))
    )
    g.add((gsteiner, RDF.type, acdh_ns.Person))

    g.add(
        (pbecker, acdh_ns.hasTitle, Literal("Peter Becker", lang='de'))
    )
    g.add(
        (pbecker, acdh_ns.hasFirstName, Literal("Peter", lang="de"))
    )
    g.add(
        (pbecker, acdh_ns.hasLastName, Literal("Becker", lang="de"))
    )
    g.add(
        (tstockinger, acdh_ns.hasTitle, Literal("Thomas Stockinger", lang='de'))
    )
    g.add(
        (tstockinger, acdh_ns.hasFirstName, Literal("Thomas", lang="de"))
    )
    g.add(
        (tstockinger, acdh_ns.hasLastName, Literal("Stockinger", lang="de"))
    )
    g.add(
        (pandorfer, acdh_ns.hasTitle, Literal("Peter Andorfer", lang='de'))
    )
    g.add((univie, RDF.type, acdh_ns.Organisation))
    g.add(
        (univie, acdh_ns.hasTitle, Literal("Universität Wien", lang='de'))
    )

    g.add(
        (
            sub,
            acdh_ns.hasDescription,
            Literal(f"{PROJECT_METADATA['description']}", lang=ARCHE_LANG))
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
        (sub, acdh_ns.hasContributor, pbecker)
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
            f"{res}",
            lang=ARCHE_LANG)
        )
    )
    g.add((sub, RDF.type, acdh_ns.Resource))
    g.add(
        (
            sub,
            acdh_ns.hasNonLinkedIdentifier,
            Literal(
                f"{res.signature}",
                lang=ARCHE_LANG)
            )
    )
    col = Graph()
    col_sub = URIRef(f"{ARCHE_BASE_URL}")
    g.add((col_sub, RDF.type, acdh_ns.TopCollection))
    col.add(
        (
            col_sub,
            acdh_ns.hasTitle,
            Literal(
                "Große Transformation",
                lang='de')
            )
    )
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
    if res.not_before is not None:
        g.add(
            (sub, acdh_ns.hasCoverageStartDate, Literal(res.not_before, datatype=XSD.date))
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
        g = g + pl
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
            (p_uri, acdh_ns.hasTitle, Literal(f"{x}", lang="und"))
        )
        if x.biography:
            p.add(
                (p_uri, acdh_ns.hasDescription, Literal(f"{x.biography}", lang="de"))
            )
        g.add(
            (sub, acdh_ns.hasActor, p_uri)
        )
        g = g + p
    # for x in res.get_waren_einheiten['waren']:
    #     g.add(
    #         (sub, acdh_ns.hasSubject, Literal(x.name, lang=ARCHE_LANG))
    #     )
    g.add(
        (
            sub,
            acdh_ns.hasCategory,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei"))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            col.add()
            g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
            col.add((col_sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
        if arche_prop_domain == 'string':
            g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
            col.add((col_sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
        else:
            g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
            col.add((col_sub, acdh_ns[const[0]], URIRef(const[1])))
    g = g + col
    return g
