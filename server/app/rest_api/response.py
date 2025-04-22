from typing import Any

import json  # Import JSON for parsing serialized JSON-LD
from enum import Enum

from fastapi import Response
from rdflib import Graph as RDFGraph
from rdflib.namespace import DCAT, DCTERMS, FOAF, SKOS, XSD

from ..core.namespace import DCATAP, DSPACE, SPDX

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


class Frame(Enum):
    SINGLE = {
        "@context": CONTEXT,
        "@type": {},
    }
    MULTIPLE = {
        "@context": CONTEXT,
    }


class JSONLDResponse(Response):
    media_type = "application/ld+json"

    def __init__(
        self,
        content: Any,  # Accept either a single Graph or a list of Graphs
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        frame: Frame | None = None,  # Use the Frame enum
        **kwargs: Any,
    ) -> None:
        # Handle single graph case
        if isinstance(content, RDFGraph):
            # Serialize the single graph to JSON-LD
            json_ld_data = content.serialize(format="json-ld", indent=4)
            json_ld_dict = json.loads(json_ld_data)

            # Ensure json_ld_dict is a dictionary
            if isinstance(json_ld_dict, list) and len(json_ld_dict) == 1:
                # If the serialized data is a list with one item, extract the item
                json_ld_dict = json_ld_dict[0]

            # Add @context at the top level
            json_ld_dict["@context"] = {"@vocab": str(DSPACE), **CONTEXT}
            self.content = json_ld_dict

        # Handle multiple graphs case (including empty list)
        elif isinstance(content, list):
            aggregated_graph = RDFGraph()

            # Combine all graphs into a single aggregated graph
            for graph in content:
                if isinstance(graph, RDFGraph):
                    aggregated_graph += graph

            # Serialize the aggregated graph to JSON-LD
            json_ld_data = aggregated_graph.serialize(format="json-ld", indent=4)
            json_ld_dict = json.loads(json_ld_data)

            # Ensure json_ld_dict is a dictionary
            if isinstance(json_ld_dict, list):
                json_ld_dict = {"@graph": json_ld_dict}

            # Remove @context from each item in the @graph
            graph_items = json_ld_dict.get("@graph", [])
            for item in graph_items:
                if "@context" in item:
                    del item["@context"]

            # Construct the final JSON-LD response
            final_json_ld = {
                "@context": {"@vocab": str(DSPACE), **CONTEXT},
                "@graph": graph_items,
            }
            self.content = final_json_ld

        else:
            raise Exception(
                "The content must be an instance of rdflib.Graph "
                "or a list of rdflib.Graph objects."
            )

        super().__init__(
            content=json.dumps(
                self.content, indent=4
            ),  # Serialize the JSON-LD back to a string
            status_code=status_code,
            headers=headers,
            **kwargs,
        )
