from typing import Annotated

from classy_fastapi import Routable, post
from fastapi import Depends

from app.core import entities, usecases

from ..depends import get_user
from ..examples import catalog_filters_example, decentralized_catalog_filters_example
from ..response import JSONLDResponse
from ..serializers import CatalogFilters
from ..tags import Tags


def get_usecases():
    """
    Dependency to get the usecases instance.
    """
    return usecases.SearchUsecases()


class SearchRoutes(Routable):
    @post(
        "/search-catalog/",
        operation_id="search_catalog",
        name="Search Local Catalog",
        tags=[Tags.Local_search],
        response_class=JSONLDResponse,
        responses={
            200: {
                "description": "Successful Response",
                "content": {
                    "application/ld+json": {
                        "example": catalog_filters_example,
                    },
                },
            }
        },
    )
    async def search_catalog(
        self,
        filters: CatalogFilters,
        user: Annotated[entities.Person, Depends(get_user)],
        usecases: usecases.SearchUsecases = Depends(get_usecases),
    ) -> JSONLDResponse:
        """
        Search the local catalog with dataset list.

        The request accepts filters as a JSON-LD object in the body.

        ### Format:
        Filters are structured as nested JSON-LD objects. Each filter defines the path
        to the field with optional operators or language annotations.

        ```json
        {
          "@context": {
            "@vocab": "http://data-space.org/",
            "<namespace>": "<namespaceURL>",
            ...
          }
          "@type": "Filters",
          "filters": [
            {
              ["@type": "<[namespace:]Class>",]
              "<[namespace:]attribute>[@<lang>]": <nestedObject> | <value> | {
                "operation": "<operator>",
                "operationValue": <value>
              }
            },
            ...
          ]
        }
        ```

        ### Supported operators:
        - `gte`, `lte` — range filtering
        - `in` — list filtering
        - `contains` — substring search

        ### Example:
        ```json
        {
          "@context": {
            "@vocab": "http://data-space.org/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "med": "http://med.example.org/"
          },
          "@type": "Filters",
          "filters": [
            {
              "dcat:dataset": {
                "extraMetadata": {
                  "@type": "med:Diagnoses",
                  "med:hasDiagnosis": {
                    "med:code": {
                      "operation": "contains",
                      "operationValue": "I10"
                    }
                  }
                }
              }
            }
          ]
        }
        ```

        ### More filter examples:
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title": "example"
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title@en": "example"
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title": {
                        "@language": "en"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title": {
                        "@value": "example"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcat:distribution": {
                        "dcat:format": "PDF"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:sex": "M"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "@type": "med:Patient",
                        "med:sex": "M"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": 75
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "@value": 75
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "@type": "xsd:integer"
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:datePublished": {
                        "operationValue": "2021-01-01",
                        "operation": "gte"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:datePublished": {
                        "operationValue": "2021-12-31",
                        "operation": "lte"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "operationValue": 70,
                            "operation": "gte"
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "operationValue": 70,
                            "operation": "lte"
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcat:keyword": {
                        "operationValue": ["science", "health"],
                        "operation": "in"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title@en": {
                        "operationValue": "example",
                        "operation": "contains"
                    }
                }
            }
          ```

        """
        response = await usecases.query_local_catalog(filters)
        return JSONLDResponse(
            content=response,
            status_code=200,
        )

    @post(
        "/search/",
        operation_id="decentralized_search",
        name="Search Local Catalog",
        tags=[Tags.Decentralized_search],
        response_class=JSONLDResponse,
        responses={
            200: {
                "description": "Successful Response",
                "content": {
                    "application/ld+json": {
                        "example": decentralized_catalog_filters_example,
                    },
                },
            }
        },
    )
    async def search_across_catalogs(
        self,
        filters: CatalogFilters,
        user: Annotated[entities.Person, Depends(get_user)],
        usecases: usecases.SearchUsecases = Depends(get_usecases),
    ) -> JSONLDResponse:
        """
        Search the across catalogs with dataset list.

        The request accepts filters as a JSON-LD object in the body.

        ### Format:
        Filters are structured as nested JSON-LD objects. Each filter defines the path
        to the field with optional operators or language annotations.

        ```json
        {
          "@context": {
            "@vocab": "http://data-space.org/",
            "<namespace>": "<namespaceURL>",
            ...
          }
          "@type": "Filters",
          "filters": [
            {
              ["@type": "<[namespace:]Class>",]
              "<[namespace:]attribute>[@<lang>]": <nestedObject> | <value> | {
                "operation": "<operator>",
                "operationValue": <value>
              }
            },
            ...
          ]
        }
        ```

        ### Supported operators:
        - `gte`, `lte` — range filtering
        - `in` — list filtering
        - `contains` — substring search

        ### Example:
        ```json
        {
          "@context": {
            "@vocab": "http://data-space.org/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "med": "http://med.example.org/"
          },
          "@type": "Filters",
          "filters": [
            {
              "dcat:dataset": {
                "extraMetadata": {
                  "@type": "med:Diagnoses",
                  "med:hasDiagnosis": {
                    "med:code": {
                      "operation": "contains",
                      "operationValue": "I10"
                    }
                  }
                }
              }
            }
          ]
        }
        ```

        ### More filter examples:
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title": "example"
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title@en": "example"
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title": {
                        "@language": "en"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title": {
                        "@value": "example"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcat:distribution": {
                        "dcat:format": "PDF"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:sex": "M"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "@type": "med:Patient",
                        "med:sex": "M"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": 75
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "@value": 75
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "@type": "xsd:integer"
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:datePublished": {
                        "operationValue": "2021-01-01",
                        "operation": "gte"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:datePublished": {
                        "operationValue": "2021-12-31",
                        "operation": "lte"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "operationValue": 70,
                            "operation": "gte"
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "med:weight": {
                            "operationValue": 70,
                            "operation": "lte"
                        }
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcat:keyword": {
                        "operationValue": ["science", "health"],
                        "operation": "in"
                    }
                }
            }
          ```
        - ```json
            {
                "dcat:dataset": {
                    "dcterms:title@en": {
                        "operationValue": "example",
                        "operation": "contains"
                    }
                }
            }
          ```

        """
        response = await usecases.aggregate_catalog_responses(filters)
        return JSONLDResponse(
            content=response,
            status_code=200,
        )


routes = SearchRoutes()
