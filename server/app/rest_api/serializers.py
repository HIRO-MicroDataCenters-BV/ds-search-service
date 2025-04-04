from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    """
    Health check response model.
    """

    status: str = Field(examples=["OK"])
