from pydantic import BaseModel, ConfigDict, Field

from .examples import catalog_filters_example


class HealthCheck(BaseModel):
    """Health check response model"""

    status: str = Field(examples=["OK"])


class JsonLD(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )


class CatalogFilters(JsonLD):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                catalog_filters_example,
            ],
        },
    )
