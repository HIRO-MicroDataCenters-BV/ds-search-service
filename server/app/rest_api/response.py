from typing import Any

import json

from fastapi import Response
from pyld import jsonld
from rdflib import Graph
from rdflib.namespace import DCAT, DCTERMS, FOAF, SKOS, XSD, Namespace

DSPACE = Namespace("http://data-space.org/")
SPDX = Namespace("http://spdx.org/rdf/terms#")
DCATAP = Namespace("http://data.europa.eu/r5r/")

CONTEXT = {
    "@vocab": str(DSPACE),
    "xsd": str(XSD),
    "dcat": str(DCAT),
    "dcatap": str(DCATAP),
    "dcterms": str(DCTERMS),
    "spdx": str(SPDX),
    "foaf": str(FOAF),
    "skos": str(SKOS),
}
RDF_TYPE = "dcat:Catalog"


class JSONLDResponse(Response):
    media_type = "application/ld+json"

    def __init__(
        self,
        content: Graph,
        rdf_type: str = RDF_TYPE,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        if not isinstance(content, Graph):
            raise Exception("The content must be an instance of rdflib.Graph")

        try:
            json_ld = self.to_json_ld(content, rdf_type)
        except Exception as e:
            raise ValueError(f"Framing failed: {e}")

        super().__init__(
            content=json_ld,
            status_code=status_code,
            headers=headers,
            **kwargs,
        )

    def to_json_ld(self, graph: Graph, rdf_type: str) -> str:
        frame = {
            "@context": CONTEXT,
            "@type": rdf_type,
        }
        json_ld_str = graph.serialize(format="json-ld")
        json_ld = json.loads(json_ld_str)
        framed_json_ld = jsonld.frame(json_ld, frame)
        return json.dumps(framed_json_ld, indent=4)
