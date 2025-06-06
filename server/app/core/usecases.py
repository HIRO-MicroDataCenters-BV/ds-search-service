from typing import Any

import json
import logging
from abc import ABC, abstractmethod

import httpx
from rdflib import Graph

from ..rest_api.serializers import CatalogFilters
from .discovery import IDiscoveryService

logger = logging.getLogger(__name__)


class ISearchUsecases(ABC):
    @abstractmethod
    async def local_search(self, query: CatalogFilters) -> Graph:
        ...

    @abstractmethod
    async def distributed_search(self, query: CatalogFilters) -> Graph:
        ...


class SearchUsecases(ISearchUsecases):
    def __init__(
        self,
        catalog_service_url: str,
        request_timeout: float,
        discovery_service: IDiscoveryService,
    ) -> None:
        self._catalog_service_url = catalog_service_url
        self._discovery_service = discovery_service
        self._request_timeout = request_timeout

    async def _post_catalog_query(
        self,
        url: str,
        endpoint: str,
        query_jsonld: dict[str, Any],
    ) -> Graph:
        """
        Internal helper to POST a catalog query and parse the JSON-LD
        response into an RDF Graph.
        """
        headers = {
            "accept": "application/ld+json",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{url}{endpoint}",
                    json=query_jsonld,
                    headers=headers,
                    timeout=self._request_timeout,
                )
                response.raise_for_status()
                rdf_graph = Graph()
                rdf_graph.parse(data=json.dumps(response.json()), format="json-ld")
                logger.info(f"Successfully queried {url}{endpoint}")
                return rdf_graph
            except Exception as exc:
                logger.error(f"Query failed at {url}{endpoint}: {exc}")
                return Graph()

    async def _query_peer_services(
        self,
        url: str,
        endpoint: str,
        query: CatalogFilters,
    ) -> Graph:
        """
        Query the peer search services with the given filters and limit.
        """
        logger.info(f"Querying peer service at {url}")
        query_jsonld = query.model_dump(by_alias=True)
        logger.debug(f"Query JSON-LD: {query_jsonld}")
        return await self._post_catalog_query(url, endpoint, query_jsonld)

    async def local_search(self, query: CatalogFilters) -> Graph:
        """Query the local public catalog with the given filters"""
        return await self._query_peer_services(
            self._catalog_service_url, "/public-catalog/", query
        )

    async def distributed_search(self, query: CatalogFilters) -> Graph:
        """
        Aggregate responses from the peer services.
        Returns a list of Graph objects containing all aggregated results.
        """

        logger.info("Starting aggregation of catalog responses")

        peer_services = await self._discovery_service.discover()
        logger.info(f"Discovered {len(peer_services)} peer services: {peer_services}")

        result_graph = Graph()
        for url in peer_services:
            service_graph = await self._query_peer_services(
                url, "/local-search/", query
            )
            result_graph += service_graph

        return result_graph
