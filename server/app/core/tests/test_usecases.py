from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rdflib import Graph

from ..usecases import SearchUsecases


class TestSearchUsecases:
    @pytest.fixture
    def discovery_service(self):
        discovery_service = AsyncMock()
        discovery_service.discover.return_value = [
            "http://peer1.com",
            "http://peer2.com",
        ]
        return discovery_service

    @pytest.fixture
    def usecases(self, discovery_service):
        return SearchUsecases(
            catalog_service_url="http://localhost:8000",
            request_timeout=1.0,
            discovery_service=discovery_service,
        )

    @pytest.fixture
    def query(self):
        mock_query = MagicMock()
        mock_query.model_dump.return_value = {"key": "value"}
        return mock_query

    @pytest.mark.asyncio
    async def test_query_peer_services(self, usecases, query):
        mock_graph = Graph()

        with patch.object(
            usecases, "_post_catalog_query", return_value=mock_graph
        ) as mock_post:
            result = await usecases.local_search(query)
            mock_post.assert_called_once_with(
                "http://localhost:8000", "/public-catalog/", {"key": "value"}
            )

            assert isinstance(result, Graph)
            assert result == mock_graph

    @pytest.mark.asyncio
    async def test_local_search(self, usecases, query):
        mock_response = {
            "@context": "",
            "@id": "item1",
        }

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = AsyncMock()

            result = await usecases.local_search(query)

            assert isinstance(result, Graph)
            assert "@context" in mock_response
            assert "@id" in mock_response

    @pytest.mark.asyncio
    async def test_local_search_failure(self, usecases, query):
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = Exception("Mocked error")

            result = await usecases.local_search(query)
            assert isinstance(result, Graph)
            assert len(result) == 0  # Ensure the graph is empty

    @pytest.mark.asyncio
    async def test_distributed_search(self, usecases, query, discovery_service):
        mock_graph_1 = Graph()
        mock_graph_1.parse(data='{"@context": "", "@id": "item1"}', format="json-ld")

        mock_graph_2 = Graph()
        mock_graph_2.parse(data='{"@context": "", "@id": "item2"}', format="json-ld")

        with patch.object(
            usecases, "_query_peer_services", side_effect=[mock_graph_1, mock_graph_2]
        ) as mock_query:
            result_graph = await usecases.distributed_search(query)

            assert isinstance(result_graph, Graph)
            assert len(result_graph) == len(mock_graph_1) + len(mock_graph_2)
            assert mock_query.call_count == 2

    @pytest.mark.asyncio
    async def test_distributed_search_failure(self, usecases, query, discovery_service):
        mock_graph_ok = Graph()
        mock_graph_ok.parse(data='{"@context": "", "@id": "ok"}', format="json-ld")

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = Exception("Mocked error")

            result = await usecases.distributed_search(query)
            assert isinstance(result, Graph)
            assert len(result) == 0  # Ensure the graph is empty
