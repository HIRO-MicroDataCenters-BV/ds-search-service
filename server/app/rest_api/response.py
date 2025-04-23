from typing import Any, List

import json

from fastapi import Response
from pyld import jsonld
from rdflib import Graph
from rdflib.namespace import DCAT, DCTERMS, FOAF, SKOS, XSD

from ..core.namespace import DCATAP, DSPACE, SPDX

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


class JSONLDResponse(Response):
    media_type = "application/ld+json"

    def __init__(
        self,
        content: Graph | List[Graph],
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        res = None
        if isinstance(content, Graph):
            res = self.to_json_ld(content)

        elif isinstance(content, list) and all(
            isinstance(item, Graph) for item in content
        ):
            all_graphs = []

            for single_graph in content:
                if single_graph:
                    graph_res = self.to_json_ld(single_graph)
                    graph_res.pop("@context", None)
                    all_graphs.append(graph_res)

            res = {"@context": CONTEXT, "@graph": all_graphs}

        else:
            raise Exception(
                "The content must be an instance of rdflib.Graph "
                "or a list of rdflib.Graph objects."
            )

        # Serialize the final content
        super().__init__(
            content=json.dumps(res, indent=4),
            status_code=status_code,
            headers=headers,
            **kwargs,
        )

    def to_json_ld(self, graph: Graph) -> dict[str, Any]:
        """
        Convert the RDF graph to JSON-LD format.
        """
        frame = {"@context": CONTEXT, "@type": "dcat:Catalog"}
        json_ld_str = graph.serialize(format="json-ld")
        json_ld = json.loads(json_ld_str)
        try:
            framed_result = jsonld.frame(json_ld, frame)
            return dict(framed_result)
        except Exception as e:
            raise ValueError(f"Framing failed: {e}")
