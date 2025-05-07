from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Reventa API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "reventa"
    DATABASE_URL: str | None = None

    # Security settings
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # Default to local frontend
    ENVIRONMENT: str = "development"  # development, staging, production

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    @property
    def cors_origins(self) -> list[str]:
        if self.ENVIRONMENT == "production":
            return self.BACKEND_CORS_ORIGINS
        elif self.ENVIRONMENT == "staging":
            return [*self.BACKEND_CORS_ORIGINS, "http://staging.example.com"]
        else:  # development
            return ["*"]  # Allow all origins in development

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
