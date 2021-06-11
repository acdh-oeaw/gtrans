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
    sub = URIRef(f"{ARCHE_BASE_URL}/aschach")
    g.add((sub, RDF.type, acdh_ns.Collection))
    g.add(
        (sub, acdh_ns.hasCoverageStartDate, Literal('1652-01-01', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasCoverageEndDate, Literal('1740-12-31', datatype=XSD.date))
    )
    g.add(
        (sub, acdh_ns.hasTitle, Literal(f"{PROJECT_METADATA['title']}", lang=ARCHE_LANG))
    )
    # define persons
    prauscher = URIRef("https://d-nb.info/gnd/13140007X")
    bpamperl = URIRef("https://d-nb.info/gnd/103048337X")
    aserles = URIRef("https://d-nb.info/gnd/1031446176")
    g.add(
        (prauscher, acdh_ns.hasTitle, Literal("Peter Rauscher", lang=ARCHE_LANG))
    )
    g.add(
        (prauscher, acdh_ns.hasFirstName, Literal("Peter", lang=ARCHE_LANG))
    )
    g.add(
        (prauscher, acdh_ns.hasLastName, Literal("Rauscher", lang=ARCHE_LANG))
    )
    g.add((prauscher, RDF.type, acdh_ns.Person))
    g.add(
        (aserles, acdh_ns.hasTitle, Literal("Andrea Serles", lang=ARCHE_LANG))
    )
    g.add(
        (aserles, acdh_ns.hasFirstName, Literal("Andrea", lang=ARCHE_LANG))
    )
    g.add(
        (aserles, acdh_ns.hasLastName, Literal("Serles", lang=ARCHE_LANG))
    )
    g.add((aserles, RDF.type, acdh_ns.Person))
    g.add(
        (bpamperl, acdh_ns.hasTitle, Literal("Beate Pamperl", lang=ARCHE_LANG))
    )
    g.add(
        (bpamperl, acdh_ns.hasFirstName, Literal("Beate", lang=ARCHE_LANG))
    )
    g.add(
        (bpamperl, acdh_ns.hasLastName, Literal("Pamperl", lang=ARCHE_LANG))
    )
    g.add((bpamperl, RDF.type, acdh_ns.Person))
    g.add(
        (
            sub,
            acdh_ns.hasDescription,
            Literal(f"{PROJECT_METADATA['description']}", lang=ARCHE_LANG))
    )
    for const in ARCHE_CONST_MAPPINGS:
        arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
        if arche_prop_domain == 'date':
            col.add()
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
    for x in res.mentioned_person.all():
        p = Graph()
        p_uri = URIRef(x.arche_id())
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
    # for const in ARCHE_CONST_MAPPINGS:
    #     arche_prop_domain = ARCHE_PROPS_LOOKUP.get(const[0], 'No Match')
    #     if arche_prop_domain == 'date':
    #         col.add()
    #         g.add((sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
    #         col.add((col_sub, acdh_ns[const[0]], Literal(const[1], datatype=XSD.date)))
    #     if arche_prop_domain == 'string':
    #         g.add((sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
    #         col.add((col_sub, acdh_ns[const[0]], Literal(const[1], lang=ARCHE_LANG)))
    #     else:
    #         g.add((sub, acdh_ns[const[0]], URIRef(const[1])))
    #         col.add((col_sub, acdh_ns[const[0]], URIRef(const[1])))
    g = g + col
    return g
