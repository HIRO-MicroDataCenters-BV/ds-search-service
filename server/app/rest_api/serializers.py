from typing import Any

from pydantic import BaseModel, Field

from .examples import catalog_filters_example


class HealthCheck(BaseModel):
    """
    Health check response model.
    """

    status: str = Field(examples=["OK"])


class JsonLD(BaseModel):
    context: dict[str, Any] = Field(None, alias="@context")

    class Config:
        populate_by_name = True
        extra = "allow"


class CatalogFilters(JsonLD):
    # TODO: Validate the data

    model_config = {
        "json_schema_extra": {
            "examples": [
                catalog_filters_example,
            ],
        },
    }
