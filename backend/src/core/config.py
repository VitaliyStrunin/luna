from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )
    
    # database settings
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_HOST: str = Field(default="postgres")
    DB_PORT: int = Field(default=5433, ge=1, le=65535)
    DB_NAME: str = Field(default="luna_db")
    
    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
    # API settings
    API_KEY: str
    
    # RabbitMQ settings
    RABBIT_USER: str = Field(default="guest")
    RABBIT_PASSWORD: str = Field(default="guest")
    RABBIT_HOST: str = Field(default="rabbitmq")
    RABBIT_PORT: int = Field(default=5672, ge=1, le=65536)
    RABBIT_VHOST: str = Field(default="")
    
    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.RABBIT_USER}:"
            f"{self.RABBIT_PASSWORD}@"
            f"{self.RABBIT_HOST}:"
            f"{self.RABBIT_PORT}"
            f"/{self.RABBIT_VHOST}"
        )
    
settings = Settings()