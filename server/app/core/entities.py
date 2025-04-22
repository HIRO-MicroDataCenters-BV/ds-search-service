from typing import Any, Self, TypedDict, cast

import json
import uuid

from pyld import jsonld
from rdflib import RDF
from rdflib import Graph as RDFGraph
from rdflib import Literal, URIRef
from rdflib.compare import to_isomorphic
from rdflib.namespace import DCAT, DCTERMS, FOAF, SKOS, XSD

from .exceptions import NodeDoesNotExist
from .namespace import DCATAP, DSPACE, SPDX

CONTEXT = {
    "dspace": str(DSPACE),
    "xsd": str(XSD),
    "dcat": str(DCAT),
    "dcatap": str(DCATAP),
    "dcterms": str(DCTERMS),
    "spdx": str(SPDX),
    "foaf": str(FOAF),
    "skos": str(SKOS),
}


class Person(TypedDict):
    id: str
    name: str


class Graph:
    rdf_type: URIRef
    label: str
    context = CONTEXT

    def __init__(self, graph: RDFGraph | None = None) -> None:
        self.graph = RDFGraph() if graph is None else graph

        for prefix, uri in self.context.items():
            self.graph.bind(prefix, uri)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        required_attrs = ["rdf_type", "label", "context"]
        for attr in required_attrs:
            if not hasattr(cls, attr):
                raise TypeError(f"Class {cls.__name__} must have attribute {attr}")

    def __str__(self) -> str:
        return self.graph.serialize(format="json-ld", indent=4, context=self.context)

    def __add__(self, other):
        """Merge two graphs into one"""
        if not isinstance(other, Graph):
            raise TypeError("Cannot add non-graph object")
        self.graph += other.graph
        return self

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Graph):
            return False
        return (
            to_isomorphic(self.graph) == to_isomorphic(other.graph)
            and self.rdf_type == other.rdf_type
            and self.label == other.label
            and self.context == other.context
        )

    @classmethod
    def create_empty(cls, id: str) -> Self:
        instance = cls()
        node = URIRef(id)
        instance.graph.add((node, RDF.type, cls.rdf_type))
        return instance

    @classmethod
    def from_json_ld(cls, json_ld: str) -> Self:
        instance = cls()
        instance.graph.parse(data=json_ld, format="json-ld")
        rdf_type = json.loads(json_ld).get("@type")
        if rdf_type:
            # Resolve the prefixed name to a full URI
            prefix, local_name = rdf_type.split(":")
            namespace = instance.graph.namespace_manager.store.namespace(prefix)
            if namespace:
                instance.rdf_type = URIRef(namespace + local_name)
            else:
                raise ValueError(
                    f"Prefix '{prefix}' not found in the namespace manager."
                )
        else:
            raise ValueError("The JSON-LD data does not contain an '@type' field.")
        return instance

    def to_json_ld(self) -> str:
        frame = {
            "@context": self.context,
            "@type": self.graph.namespace_manager.qname(self.rdf_type),
        }
        json_ld_str = self.graph.serialize(format="json-ld")
        json_ld = json.loads(json_ld_str)
        framed_json_ld = jsonld.frame(json_ld, frame)
        return json.dumps(framed_json_ld, indent=4)

    @property
    def uri(self) -> URIRef:
        node = next(self.graph.subjects(RDF.type, self.rdf_type), None)
        if node is None:
            raise NodeDoesNotExist("Root node not found in the graph")
        return cast(URIRef, node)

    def get_attribute(self, attr: URIRef, default: Any = None) -> Any:
        return next(self.graph.objects(self.uri, attr), default)

    def set_attribute(
        self,
        attr: URIRef,
        value: URIRef | str | int | bool,
        datatype: URIRef | None = None,
        lang: str | None = None,
    ) -> None:
        obj: Any
        if isinstance(value, URIRef):
            obj = value
        else:
            if lang:
                obj = Literal(value, lang=lang)
            elif datatype:
                obj = Literal(value, datatype=datatype)
            else:
                obj = Literal(value)
        self.graph.add((self.uri, attr, obj))


class CatalogFilters(Graph):
    rdf_type = DSPACE.Filters
    label = "f"


class Catalog(Graph):
    rdf_type = DCAT.Catalog
    label = "c"

    @classmethod
    def create(cls, title: str, description: str) -> Self:
        id = str(uuid.uuid4())
        catalog = cls.create_empty(id)
        catalog.set_attribute(DCTERMS.identifier, id)
        catalog.set_attribute(DCTERMS.title, title)
        catalog.set_attribute(DCTERMS.description, description)
        return catalog


class Dataset(Graph):
    rdf_type = DCAT.Dataset
    label = "d"
