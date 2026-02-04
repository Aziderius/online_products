from fastapi import Header, HTTPException, status, Depends
from app.core.config import get_settings

def validate_internal_api_key(internal_api_key: str = Header(..., alias="internal-api-key")):
    settings = get_settings()

    if internal_api_key != settings.INTERNAL_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal API key"
        )
