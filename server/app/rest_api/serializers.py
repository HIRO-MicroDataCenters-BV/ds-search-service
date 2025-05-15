from typing import Any, Dict, List

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
    # Define JSON-LD fields with proper aliases
    context: Dict[str, Any] = Field(..., alias="@context")
    type: str = Field(..., alias="@type")
    filters: List[Dict[str, Any]]

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                catalog_filters_example,
            ],
        },
    }
