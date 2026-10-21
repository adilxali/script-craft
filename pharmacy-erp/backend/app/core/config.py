from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development")
    APP_NAME: str = "Pharmacy ERP SaaS"
    API_V1_STR: str = "/api/v1"
    
    # Security & JWT
    SECRET_KEY: str = Field(default="dev_insecure_super_secret_jwt_key_change_in_production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours for retail shifts
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"
    
    # Database & Cache
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://erp_admin:dev_erp_password_2026@localhost:5432/pharmacy_erp_db"
    )
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # S3 Storage (AWS / MinIO)
    S3_ENDPOINT_URL: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET_NAME: str = "pharmacy-private-storage"
    S3_REGION: str = "ap-south-1"  # Mumbai AWS Region for DPDP data residency
    
    # GST & Statutory Defaults
    DEFAULT_CURRENCY: str = "INR"
    DEFAULT_STATE_CODE: str = "27"  # Maharashtra (default reference)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
