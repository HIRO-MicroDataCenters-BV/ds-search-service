from typing import List

import logging
import socket
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class IDiscoveryService(ABC):
    @abstractmethod
    async def discover(self) -> List[str]:
        ...


class KubeDiscoveryService(IDiscoveryService):
    """Discover other search services pod using k8s DNS"""

    def __init__(
        self, namespaces: list[str], service_name: str, service_port: int
    ) -> None:
        self._namespaces = namespaces
        self._service_name = service_name
        self._service_port = service_port

    async def discover(self) -> List[str]:
        peer_services = []
        for namespace in self._namespaces:
            try:
                _, _, ips = socket.gethostbyname_ex(
                    f"{self._service_name}.{namespace}.svc.cluster.local"
                )
                services = [f"http://{ip}:{self._service_port}" for ip in ips]
                logger.info(
                    f"Discovered peer services in namespace '{namespace}': {services}"
                )
                peer_services.extend(services)
            except Exception as e:
                logger.error(
                    f"Error discovering peer services in namespace '{namespace}': {e}"
                )
        return peer_services


class DummyDiscoveryService(IDiscoveryService):
    """Dummy discovery service that returns a predefined list of search service URLs"""

    def __init__(self, search_service_urls: list[str]) -> None:
        self._search_service_urls = search_service_urls

    async def discover(self) -> List[str]:
        return self._search_service_urls
