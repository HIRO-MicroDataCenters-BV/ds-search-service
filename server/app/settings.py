from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="DS_SEARCH__",
        case_sensitive=False,
        extra="ignore",
    )

    pod_namespace: str = "default"
    service_name: str = "search-service"
    service_port: int = 8000

    catalog_service_url: str = "http://localhost:8000"
    request_timeout: float = 5.0

    discovery_type: str = "kube"
    dummy_search_service_urls: Annotated[list[str], NoDecode] = []

    @field_validator("dummy_search_service_urls", mode="before")
    @classmethod
    def parse_urls(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v


def get_settings() -> Settings:
    settings = Settings()
    return settings
