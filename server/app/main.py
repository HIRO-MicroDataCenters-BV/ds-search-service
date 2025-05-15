from typing import Any, Dict

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from prometheus_fastapi_instrumentator import Instrumentator

from app.logging_config import setup_logging
from app.rest_api.routes import health_check, search


class CustomFastAPI(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        if self.openapi_schema:
            return self.openapi_schema
        openapi_schema = get_openapi(
            title="Data Space Search Service",
            version="0.0.0",
            description="The Search Service is a service of the Data Space "
            "Node, designed to process search queries and aggregate "
            "results from decentralized catalogs.",
            contact={
                "name": "HIRO-MicroDataCenters",
                "email": "all-hiro@hiro-microdatacenters.nl",
            },
            license_info={
                "name": "MIT",
                "url": "https://github.com/HIRO-MicroDataCenters-BV"
                "/ds-search-service/blob/main/LICENSE",
            },
            routes=self.routes,
        )
        self.openapi_schema = openapi_schema
        return self.openapi_schema


setup_logging()

app = CustomFastAPI()

Instrumentator().instrument(app).expose(app)


app.include_router(health_check.routes.router)
app.include_router(search.routes.router)
