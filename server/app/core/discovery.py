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

    def __init__(self, namespace: str, service_name: str, service_port: int) -> None:
        self._namespace = namespace
        self._service_name = service_name
        self._service_port = service_port

    async def discover(self) -> List[str]:
        try:
            _, _, ips = socket.gethostbyname_ex(
                f"{self._service_name}.{self._namespace}.svc.cluster.local"
            )
            peer_services = [f"http://{ip}:{self._service_port}" for ip in ips]
            logger.info(f"Discovered peer services: {peer_services}")
            return peer_services
        except Exception as e:
            logger.error(f"Error discovering peer services: {e}")
            return []


class DummyDiscoveryService(IDiscoveryService):
    """Dummy discovery service that returns a predefined list of search service URLs"""

    def __init__(self, search_service_urls: list[str]) -> None:
        self._search_service_urls = search_service_urls

    async def discover(self) -> List[str]:
        return self._search_service_urls
