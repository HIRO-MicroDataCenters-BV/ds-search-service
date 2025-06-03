from typing import Annotated

import logging

from classy_fastapi import Routable, post
from fastapi import Depends

from app.core import entities, usecases

from ..depends import get_user
from ..examples import catalog_filters_example, decentralized_catalog_filters_example
from ..response import JSONLDResponse
from ..serializers import CatalogFilters
from ..tags import Tags

logger = logging.getLogger(__name__)


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

        for details, check ds-catalog-service documentation.

        https://hiro-microdatacenters-bv.github.io/ds-catalog/docs/index.html#tag/Catalog/operation/get_catalog

        """
        logger.info("Received request to search the local catalog")
        response = await usecases.query_local_catalog(filters)
        logger.info("Successfully queried the local catalog")
        logger.debug(f"Response type: {type(response)}, Response: {response}")
        return JSONLDResponse(
            content=response,
            status_code=200,
        )

    @post(
        "/search/",
        operation_id="decentralized_search",
        name="Decentralized Search across catalogs",
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

        for details, check ds-catalog-service documentation.
        https://hiro-microdatacenters-bv.github.io/ds-catalog/docs/index.html

        """
        logger.info("Received request to perform decentralized search across catalogs")
        responses = await usecases.aggregate_catalog_responses(filters)
        logger.info("Successfully aggregated responses from catalogs")
        logger.debug(f"Aggregated responses: {responses}")
        return JSONLDResponse(
            content=responses,  # Pass a list of graphs
            status_code=200,
        )


routes = SearchRoutes()
