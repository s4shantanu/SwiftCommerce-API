from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SwiftCommerce API"
    VERSION: str = "1.0.0"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "swiftcommerce"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # JWT
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_HERE"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Stripe
    STRIPE_API_KEY: str = "sk_test_placeholder"
    STRIPE_WEBHOOK_SECRET: str = "whsec_placeholder"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()