from classy_fastapi import Routable, get

from ..serializers import HealthCheck


class HealthCheckRoutes(Routable):
    @get(
        "/health-check",
        operation_id="health_check",
        summary="Health check",
        response_model=HealthCheck,
    )
    async def health_check(self) -> dict[str, str]:
        """Returns a 200 status code if the service is up and running"""
        return {"status": "OK"}


routes = HealthCheckRoutes()
