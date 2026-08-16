from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str = "IMEI Provenance Prototype REST Gateway"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
settings = Settings()
