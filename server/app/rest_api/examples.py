from typing import Any

context_example: dict[str, Any] = {
    "@vocab": "http://data-space.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcatap": "http://data.europa.eu/r5r/",
    "dcterms": "http://purl.org/dc/terms/",
    "spdx": "http://spdx.org/rdf/terms#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
}

dataset_body_example: dict[str, Any] = {
    "@id": "https://example.com/dataset/789",
    "@type": "dcat:Dataset",
    "any_key": "any_value",
}

catalog_filters_example: dict[str, Any] = {
    "@context": {
        "@vocab": "http://data-space.org/",
        "dcat": "http://www.w3.org/ns/dcat#",
        "dcterms": "http://purl.org/dc/terms/",
    },
    "@type": "Filters",
    "filters": [
        {
            "dcat:dataset": {
                "dcterms:identifier": "123",
            }
        }
    ],
}

decentralized_catalog_filters_example: dict[str, Any] = {
    "@context": context_example,
    "@graph": [
        {
            "@id": "https://example.com/catalog/123",
            "@type": "dcat:Catalog",
            "dcterms:title": {"@language": "en", "@value": "Sample Catalog"},
            "dcterms:description": {
                "@language": "en",
                "@value": "This is a sample catalog containing "
                "various datasets and services.",
            },
            "dcterms:publisher": {
                "@id": "https://example.com/person/123",
                "@type": "foaf:Agent",
                "foaf:name": "John Doe",
            },
            "dcat:dataset": [
                dataset_body_example,
            ],
        },
        {
            "@id": "https://example.com/catalog/456",
            "@type": "dcat:Catalog",
            "dcterms:title": {"@language": "en", "@value": "Another Catalog"},
            "dcterms:description": {
                "@language": "en",
                "@value": "This is another sample catalog.",
            },
            "dcterms:publisher": {
                "@id": "https://example.com/person/456",
                "@type": "foaf:Agent",
                "foaf:name": "Jane Smith",
            },
            "dcat:dataset": [
                dataset_body_example,
            ],
        },
    ],
}
