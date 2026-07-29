import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise IMEI Provenance REST Gateway"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Cryptographic Configuration
    ALLOWED_SIGNING_ALGORITHMS: list = ["RS256", "ES256"]
    
    # Simulated Off-Chain Ledger Sink Configuration
    DATA_LAKE_INGESTION_THRESHOLD_MB: int = 50
    POSTGRES_PORT: int = 5432
    
    class Config:
        case_sensitive = True

settings = Settings()