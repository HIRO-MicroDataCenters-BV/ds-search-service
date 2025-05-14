from typing import List

import json
import logging
import os
import socket

import httpx
from rdflib import Graph

from ..rest_api.serializers import CatalogFilters

# Module-level logger
logger = logging.getLogger(__name__)


class SearchUsecases:
    def __init__(self):
        self.namespace = os.getenv("POD_NAMESPACE", "default")
        self.service_name = os.getenv("SERVICE_NAME", "search-service")
        self.service_port = os.getenv("SERVICE_PORT", "8000")
        self.catalog_service_url = os.getenv(
            "CATALOG_SERVICE_URL", "http://localhost:8001"
        )
        self.request_timeout = os.getenv("REQUEST_TIMEOUT", 5.0)

    async def get_current_ip(self) -> str:
        """
        Get the current IP address of the machine.
        """
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            logger.info(f"Resolved IP address: {ip_address}")
        except socket.gaierror:
            logger.error("Error: Unable to resolve hostname")
            return "Unable to get IP address"
        return ip_address

    async def discover_peer_services(self) -> List[str]:
        """
        Discover other search services pod using k8s DNS
        """
        try:
            current_ip = await self.get_current_ip()
            _, _, ips = socket.gethostbyname_ex(
                f"{self.service_name}.{self.namespace}.svc.cluster.local"
            )
            peer_services = [
                f"http://{ip}:{self.service_port}" for ip in ips if ip != current_ip
            ]
            logger.info(f"Discovered peer services: {peer_services}")
            return peer_services
        except Exception as e:
            logger.error(f"Error discovering peer services: {e}")
            return []

    async def query_local_catalog(self, query: CatalogFilters) -> Graph:
        """
        Query the local catalog with the given filters and limit.
        """
        logger.info("Querying local catalog")
        query_jsonld = query.model_dump(by_alias=True)
        logger.debug(f"Query JSON-LD: {query_jsonld}")
        headers = {
            "accept": "application/ld+json",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.catalog_service_url}/catalog/",
                    json=query_jsonld,
                    headers=headers,
                    timeout=float(self.request_timeout),
                )
                response.raise_for_status()
                rdf_graph = Graph()
                rdf_graph.parse(data=json.dumps(response.json()), format="json-ld")
                logger.info("Successfully queried local catalog")
                return rdf_graph
            except Exception as exc:
                logger.error(f"Local catalog query failed: {exc}")
                return Graph()

    async def query_peer_services(self, url: str, query: CatalogFilters) -> Graph:
        """
        Query the peer search services with the given filters and limit.
        """
        logger.info(f"Querying peer service at {url}")
        query_jsonld = query.model_dump()
        headers = {
            "accept": "application/ld+json",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{url}/search-catalog/",
                    json=query_jsonld,
                    headers=headers,
                    timeout=float(self.request_timeout),
                )
                response.raise_for_status()
                rdf_graph = Graph()
                rdf_graph.parse(data=json.dumps(response.json()), format="json-ld")
                logger.info(f"Successfully queried peer service at {url}")
                return rdf_graph
            except Exception as exc:
                logger.error(f"Peer catalog query failed at {url}: {exc}")
                return Graph()

    async def aggregate_catalog_responses(self, query: CatalogFilters) -> List[Graph]:
        """
        Aggregate responses from the local catalog and peer services.
        Returns a list of Graph objects containing all aggregated results.
        """
        logger.info("Starting aggregation of catalog responses")

        # Query the local catalog
        local_response = await self.query_local_catalog(query)
        logger.debug(f"Local response: {local_response.serialize(format='json-ld')}")

        # Discover and query peer services
        peer_services = await self.discover_peer_services()
        logger.info(f"Discovered {len(peer_services)} peer services: {peer_services}")
        peer_responses = [
            await self.query_peer_services(url, query) for url in peer_services
        ]
        logger.info(f"Received {len(peer_responses)} responses from peer services")

        # Combine all responses into a list of Graphs
        aggregated_graphs = [local_response]
        aggregated_graphs.extend(peer_responses)

        logger.info(f"Aggregated {len(aggregated_graphs)} graphs in total")
        return aggregated_graphs
