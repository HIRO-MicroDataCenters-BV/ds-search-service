import socket
from unittest.mock import patch

import pytest

from ..discovery import DummyDiscoveryService, KubeDiscoveryService


class TestDummyDiscoveryService:
    @pytest.mark.asyncio
    async def test_common(self):
        urls = ["http://service1:8080", "http://service2:8080"]
        service = DummyDiscoveryService(urls)
        discovered = await service.discover()
        assert discovered == urls


class TestKubeDiscoveryService:
    @pytest.mark.asyncio
    async def test_common(self):
        peers_namespaces = ["default"]
        service_name = "my-service"
        service_port = 8080
        other_ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

        service = KubeDiscoveryService(peers_namespaces, service_name, service_port)

        with patch("socket.gethostbyname_ex", return_value=("fqdn", [], other_ips)):
            discovered = await service.discover()
            assert discovered == [
                f"http://10.0.0.1:{service_port}",
                f"http://10.0.0.2:{service_port}",
                f"http://10.0.0.3:{service_port}",
            ]

    @pytest.mark.asyncio
    async def test_failure(self):
        service = KubeDiscoveryService(["default"], "my-service", 8080)
        with patch(
            "socket.gethostbyname_ex", side_effect=socket.gaierror("test error")
        ):
            result = await service.discover()
            assert result == []
