from typing import Any, Dict

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from rdflib import Graph

from app.core.tests.factories import person_factory
from app.main import app  # Import the FastAPI app instance
from app.rest_api.routes.search import get_usecases

from ...serializers import CatalogFilters

client = TestClient(app)  # Use the app instance instead of the router


@patch("app.rest_api.routes.search.get_user")
@patch("app.rest_api.routes.search.get_usecases")
def test_search_catalog(mock_get_usecases, mock_get_user):
    """
    Test the /search-catalog/ endpoint.
    """
    # Mock dependencies
    mock_user = person_factory()
    mock_get_user.return_value = mock_user

    mock_usecases = AsyncMock()

    # Create a mocked rdflib.Graph object
    mocked_graph = Graph()
    mocked_graph.parse(
        data="""
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://neo4j.com/base/b3b47c94-dacd-452d-ba21-07bf93e77559> a dcat:Catalog ;
        dcterms:title "Local catalog"^^xsd:string ;
        dcterms:description "My local catalog"^^xsd:string ;
        dcterms:identifier "b3b47c94-dacd-452d-ba21-07bf93e77559"^^xsd:string .
""",
        format="turtle",
    )

    # Mock the query_local_catalog method to return the mocked graph
    mock_usecases.query_local_catalog.return_value = mocked_graph
    mock_get_usecases.return_value = mock_usecases

    # Override the dependency in the FastAPI app
    app.dependency_overrides[get_usecases] = lambda: mock_usecases

    # Define test filters
    filters: Dict[str, Any] = {
        "@context": {
            "@vocab": "http://data-space.org/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "med": "http://med.example.org/",
        },
        "@type": "Filters",
        "filters": [
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "@type": "med:Diagnoses",
                        "med:hasDiagnosis": {
                            "med:code": {
                                "operation": "contains",
                                "operationValue": "I10",
                            }
                        },
                    }
                }
            }
        ],
    }

    # Ensure the filters match the expected input for CatalogFilters
    catalog_filters = CatalogFilters(**filters)

    # Make the request
    response = client.post("/search-catalog/", json=filters)

    # Debugging: Check if the mock was called
    print("#######Mocked usecases", mock_usecases.query_local_catalog.call_args_list)

    # Assertions
    assert response.status_code == 200
    assert "@context" in response.json()
    assert "@type" in response.json()

    # Ensure the mocked method was awaited with the correct argument
    mock_usecases.query_local_catalog.assert_awaited_once_with(catalog_filters)

    # Clean up the dependency override
    app.dependency_overrides = {}


@patch("app.rest_api.routes.search.get_user")
@patch("app.rest_api.routes.search.get_usecases")
def test_search_across_catalogs(mock_get_usecases, mock_get_user):
    """
    Test the /search/ endpoint.
    """
    # Mock dependencies
    mock_user = person_factory()
    mock_get_user.return_value = mock_user

    mock_usecases = AsyncMock()

    # Create mocked rdflib.Graph objects
    mocked_graph_1 = Graph()
    mocked_graph_1.parse(
        data="""
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://neo4j.com/base/b3b47c94-dacd-452d-ba21-07bf93e77559> a dcat:Catalog ;
        dcterms:title "Local catalog"^^xsd:string ;
        dcterms:description "My local catalog1"^^xsd:string ;
        dcterms:identifier "c3c47c94-dacd-452d-ba21-07bf93e77559"^^xsd:string .
""",
        format="turtle",
    )

    mocked_graph_2 = Graph()
    mocked_graph_2.parse(
        data="""
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://neo4j.com/base/b3b47c94-dacd-452d-ba21-07bf93e77559> a dcat:Catalog ;
        dcterms:title "Local catalog2"^^xsd:string ;
        dcterms:description "My local catalog"^^xsd:string ;
        dcterms:identifier "b3b47c94-dacd-452d-ba21-07bf93e77559"^^xsd:string .
""",
        format="turtle",
    )

    # Mock the aggregate_catalog_responses method to return a list of mocked graphs
    mock_usecases.aggregate_catalog_responses.return_value = [
        mocked_graph_1,
        mocked_graph_2,
    ]
    mock_get_usecases.return_value = mock_usecases

    # Override the dependency in the FastAPI app
    app.dependency_overrides[get_usecases] = lambda: mock_usecases

    # Define test filters
    filters: Dict[str, Any] = {
        "@context": {
            "@vocab": "http://data-space.org/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "med": "http://med.example.org/",
        },
        "@type": "Filters",
        "filters": [
            {
                "dcat:dataset": {
                    "extraMetadata": {
                        "@type": "med:Diagnoses",
                        "med:hasDiagnosis": {
                            "med:code": {
                                "operation": "contains",
                                "operationValue": "I10",
                            }
                        },
                    }
                }
            }
        ],
    }

    # Ensure the filters match the expected input for CatalogFilters
    catalog_filters = CatalogFilters(**filters)

    # Make the request
    response = client.post("/search/", json=filters)

    # Assertions
    assert response.status_code == 200
    assert len(response.json()) == 2  # Ensure two graphs are returned
    assert "@context" in response.json()
    assert "@graph" in response.json()

    # Ensure the mocked method was awaited with the correct argument
    mock_usecases.aggregate_catalog_responses.assert_awaited_once_with(catalog_filters)

    # Clean up the dependency override
    app.dependency_overrides = {}
