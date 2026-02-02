"""Configuration from environment - no hardcoded credentials."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "local"

    # Asset Registry (PostgreSQL)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "ecp"
    postgres_password: str = "changeme"
    postgres_db: str = "ecp_registry"
    database_url: str | None = None

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"

    # Vector store
    vector_store_type: str = "pgvector"
    pgvector_connection_string: str = "postgresql://ecp:changeme@localhost:5432/ecp_vectors"

    # Cube
    cube_api_url: str = "http://localhost:4000/cubejs-api/v1"
    cube_api_token: str = ""

    # OPA
    opa_url: str = "http://localhost:8181/v1"
    opa_data_path: str = "data_access"
    opa_policy_path: str = "ecp/data_access"

    # Resolution
    resolution_cache_ttl_seconds: int = 3600
    resolution_log_level: str = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    mcp_port: int = 3000

    # Observability
    log_level: str = "INFO"
    otel_exporter_otlp_endpoint: str = ""
    trace_sample_rate: float = 0.1

    @property
    def registry_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sync_registry_url(self) -> str:
        if self.database_url:
            return self.database_url.replace("+asyncpg", "")
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
