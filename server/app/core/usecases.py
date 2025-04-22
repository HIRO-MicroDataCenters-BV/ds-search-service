from typing import List

import json
import os
import socket

import httpx
from rdflib import Graph

from ..rest_api.serializers import CatalogFilters


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
            # Get the hostname of the machine
            hostname = socket.gethostname()
            # Get the IP address using the hostname
            ip_address = socket.gethostbyname(hostname)
        except socket.gaierror:
            # Handle the case where the hostname could not be resolved
            print("Error: Unable to resolve hostname")
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
            # Filter out the current pod IP
            return [
                f"http://{ip}:{self.service_port}" for ip in ips if ip != current_ip
            ]
        except Exception as e:
            # Handle any exceptions that occur during the discovery process
            print(f"Error discovering peer services: {e}")
            return []

    async def query_local_catalog(self, query: CatalogFilters) -> Graph:
        """
        Query the local catalog with the given filters and limit.
        """
        # Convert the Pydantic model to a dictionary (JSON-LD format)
        print("############################query", query)
        query_jsonld = query.model_dump()
        # Define headers
        headers = {
            "accept": "application/ld+json",  # Specify JSON-LD content type
            "Content-Type": "application/json",  # Example of an authorization header
        }
        # Implement the logic to query the local catalog
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.catalog_service_url}/catalog/",
                    json=query_jsonld,
                    headers=headers,
                    timeout=float(self.request_timeout),
                )
                response.raise_for_status()
                # Parse the JSON-LD response into a Graph instance
                rdf_graph = Graph()
                rdf_graph.parse(data=json.dumps(response.json()), format="json-ld")
                return rdf_graph
            except Exception as exc:
                print(f"Local catalog query failed: {exc}")
                # Return an empty Graph instance in case of failure
                return Graph()

    async def query_peer_services(self, url: str, query: CatalogFilters) -> Graph:
        """
        Query the peer search services with the given filters and limit.
        """
        # Convert the Pydantic model to a dictionary (JSON-LD format)
        query_jsonld = query.model_dump()
        # Define headers
        headers = {
            "accept": "application/ld+json",  # Specify JSON-LD content type
            "Content-Type": "application/json",  # Example of an authorization header
        }
        # Implement the logic to query the peer catalogs
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{url}/search_catalog/",
                    json=query_jsonld,
                    headers=headers,
                    timeout=float(self.request_timeout),
                )
                response.raise_for_status()
                # Parse the JSON-LD response into a Graph instance
                rdf_graph = Graph()
                rdf_graph.parse(data=json.dumps(response.json()), format="json-ld")
                return rdf_graph
            except Exception as exc:
                print(f"Peer catalog query failed: {exc}")
                # Return an empty Graph instance in case of failure
                return Graph()

    async def aggregate_catalog_responses(self, query: CatalogFilters) -> List[Graph]:
        """
        Aggregate responses from the local catalog and peer services.
        Returns a list of Graph objects containing all aggregated results.
        """
        print("Starting aggregation")

        # Query the local catalog
        local_response = await self.query_local_catalog(query)
        print(
            "################local_response", local_response.serialize(format="json-ld")
        )

        # Discover and query peer services
        peer_services = await self.discover_peer_services()
        peer_responses = [
            await self.query_peer_services(url, query) for url in peer_services
        ]

        # Combine all responses into a list of Graphs
        aggregated_graphs = [local_response] if local_response else []
        aggregated_graphs.extend(peer_responses)

        print("################Aggregated graphs count:", len(aggregated_graphs))
        return aggregated_graphs
