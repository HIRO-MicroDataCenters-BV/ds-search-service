import socket
from unittest.mock import AsyncMock, patch

import pytest
from rdflib import Graph

from ...rest_api.examples import catalog_filters_example
from ...rest_api.serializers import CatalogFilters
from ..usecases import SearchUsecases


@pytest.mark.asyncio
async def test_get_current_ip_success():
    """
    Test get_current_ip when the IP address is successfully retrieved.
    """
    usecases = SearchUsecases()
    mock_hostname = "test-host"
    mock_ip = "192.168.1.1"

    with patch("socket.gethostname", return_value=mock_hostname), patch(
        "socket.gethostbyname", return_value=mock_ip
    ):
        result = await usecases.get_current_ip()
        assert result == mock_ip


@pytest.mark.asyncio
async def test_get_current_ip_failure():
    """
    Test get_current_ip when hostname resolution fails.
    """
    usecases = SearchUsecases()

    with patch("socket.gethostname", return_value="test-host"), patch(
        "socket.gethostbyname", side_effect=socket.gaierror
    ):
        result = await usecases.get_current_ip()
        assert result == "Unable to get IP address"


@pytest.mark.asyncio
async def test_discover_peer_services_success():
    """
    Test discover_peer_services when peer services are successfully discovered.
    """
    usecases = SearchUsecases()
    mock_current_ip = "192.168.1.1"
    mock_ips = ["192.168.1.2", "192.168.1.3"]

    with patch.object(usecases, "get_current_ip", return_value=mock_current_ip), patch(
        "socket.gethostbyname_ex", return_value=("hostname", [], mock_ips)
    ):
        result = await usecases.discover_peer_services()
        expected = [
            f"http://{ip}:{usecases.service_port}"
            for ip in mock_ips
            if ip != mock_current_ip
        ]
        assert result == expected


@pytest.mark.asyncio
async def test_discover_peer_services_failure():
    """
    Test discover_peer_services when an exception occurs.
    """
    usecases = SearchUsecases()

    with patch.object(
        usecases, "get_current_ip", side_effect=Exception("Mocked error")
    ), patch("socket.gethostbyname_ex", side_effect=Exception("Mocked error")):
        result = await usecases.discover_peer_services()
        assert result == []


@pytest.mark.asyncio
async def test_query_local_catalog_success():
    """
    Test query_local_catalog when the query is successful.
    """
    usecases = SearchUsecases()
    mock_query = CatalogFilters(**catalog_filters_example)
    mock_response = {
        "@context": "",
        "@type": "Catalog",
    }  # Mocked response with @context and @type

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = AsyncMock()

        result = await usecases.query_local_catalog(mock_query)
        assert isinstance(result, Graph)
        # Assert the mocked response contains @context and @type
        assert "@context" in mock_response
        assert "@type" in mock_response


@pytest.mark.asyncio
async def test_query_local_catalog_failure():
    """
    Test query_local_catalog when an exception occurs.
    """
    usecases = SearchUsecases()
    mock_query = CatalogFilters(**catalog_filters_example)

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("Mocked error")

        result = await usecases.query_local_catalog(mock_query)
        assert isinstance(result, Graph)
        assert len(result) == 0  # Ensure the graph is empty


@pytest.mark.asyncio
async def test_query_peer_services_success():
    """
    Test query_peer_services when the query is successful.
    """
    usecases = SearchUsecases()
    mock_query = CatalogFilters(**catalog_filters_example)
    mock_url = "http://192.168.1.2:8000"
    mock_response = {
        "@context": "",
        "@type": "Catalog",
    }  # Mocked response with @context and @type

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = AsyncMock()

        result = await usecases.query_peer_services(mock_url, mock_query)
        assert isinstance(result, Graph)
        # Assert the mocked response contains @context and @type
        assert "@context" in mock_response
        assert "@type" in mock_response


@pytest.mark.asyncio
async def test_query_peer_services_failure():
    """
    Test query_peer_services when an exception occurs.
    """
    usecases = SearchUsecases()
    mock_query = CatalogFilters(**catalog_filters_example)
    mock_url = "http://192.168.1.2:8000"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("Mocked error")

        result = await usecases.query_peer_services(mock_url, mock_query)
        assert isinstance(result, Graph)
        assert len(result) == 0  # Ensure the graph is empty


@pytest.mark.asyncio
async def test_aggregate_catalog_responses():
    """
    Test aggregate_catalog_responses to ensure it aggregates responses correctly.
    """
    usecases = SearchUsecases()
    mock_query = CatalogFilters(**catalog_filters_example)
    mock_local_response = Graph()
    mock_peer_response = Graph()
    mock_peer_services = ["http://192.168.1.2:8000", "http://192.168.1.3:8000"]
    mock_response = {
        "@context": "",
        "@graph": "[]",
    }

    with patch.object(
        usecases, "query_local_catalog", return_value=mock_local_response
    ), patch.object(
        usecases, "discover_peer_services", return_value=mock_peer_services
    ), patch.object(
        usecases, "query_peer_services", new_callable=AsyncMock
    ) as mock_query_peer_services:
        mock_query_peer_services.return_value = mock_peer_response
        result = await usecases.aggregate_catalog_responses(mock_query)
        print("####result", result)
        assert len(result) == 3  # 1 local response + 2 peer responses
        assert all(isinstance(graph, Graph) for graph in result)
        assert "@context" in mock_response
        assert "@graph" in mock_response
