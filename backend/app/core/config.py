from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "CampusCare API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"


settings = Settings()
