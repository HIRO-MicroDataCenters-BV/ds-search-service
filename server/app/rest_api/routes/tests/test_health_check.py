from ..health_check import routes
from .helpers import create_test_client


def test_health_check() -> None:
    """
    Test the health check endpoint.
    """
    client = create_test_client(routes.router)
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_health_check_not_found() -> None:
    """
    Test the health check endpoint with a 404 status code.
    """
    client = create_test_client(routes.router)
    response = client.get("/health-check/invalid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_health_check_invalid_method() -> None:
    """
    Test the health check endpoint with an invalid method.
    """
    client = create_test_client(routes.router)
    response = client.post("/health-check")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}
