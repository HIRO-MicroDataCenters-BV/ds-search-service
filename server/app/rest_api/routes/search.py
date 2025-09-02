from typing import Annotated

import logging

from classy_fastapi import Routable, post
from fastapi import Depends

from app.core import discovery, entities, usecases
from app.settings import Settings, get_settings

from ..depends import get_user
from ..examples import catalog_filters_example, decentralized_catalog_filters_example
from ..response import JSONLDResponse
from ..serializers import CatalogFilters
from ..tags import Tags

logger = logging.getLogger(__name__)


def get_usecases(settings: Settings = Depends(get_settings)) -> usecases.SearchUsecases:
    """Dependency to get the usecases instance"""

    discovery_service: discovery.IDiscoveryService

    if settings.discovery_type == "dummy":
        discovery_service = discovery.DummyDiscoveryService(
            search_service_urls=settings.dummy_search_service_urls,
        )
    elif settings.discovery_type == "kube":
        peers_namespaces = settings.peers_namespaces
        discovery_service = discovery.KubeDiscoveryService(
            namespaces=peers_namespaces,
            service_name=settings.service_name,
            service_port=settings.service_port,
        )
    else:
        logger.error(f"Unsupported discovery type: {settings.discovery_type}")
        raise ValueError(f"Unsupported discovery type: {settings.discovery_type}")

    return usecases.SearchUsecases(
        discovery_service=discovery_service,
        catalog_service_url=settings.catalog_service_url,
        request_timeout=settings.request_timeout,
    )


class SearchRoutes(Routable):
    @post(
        "/local-search/",
        operation_id="local_search",
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
    async def local_search(
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
        response = await usecases.local_search(filters)
        logger.info("Successfully queried the local catalog")
        logger.debug(f"Response type: {type(response)}, Response: {response}")
        return JSONLDResponse(content=response, status_code=200)

    @post(
        "/distributed-search/",
        operation_id="distributed_search",
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
    async def distributed_search(
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
        responses = await usecases.distributed_search(filters)
        logger.info("Successfully aggregated responses from catalogs")
        logger.debug(f"Aggregated responses: {responses}")
        return JSONLDResponse(content=responses, status_code=200)


routes = SearchRoutes()
