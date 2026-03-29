from src.core.config import settings
from fastapi import status, Header, HTTPException


def verify_api_key(x_api_key: str = Header(alias="X-API-Key")):
    if settings.API_KEY != x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
        