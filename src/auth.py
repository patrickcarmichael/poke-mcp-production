"""Authentication and authorization module."""
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.config import settings
from src.logger import get_logger

logger = get_logger(__name__)
security = HTTPBearer()


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    """Verify API key from Authorization header.

    Args:
        credentials: HTTP authorization credentials.

    Returns:
        The API key if valid.

    Raises:
        HTTPException: If authentication fails.
    """
    if not settings.api_key:
        logger.warning("api_key_not_configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured",
        )

    if credentials.credentials != settings.api_key:
        logger.warning("invalid_api_key_attempt", provided_key=credentials.credentials[:10])
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("api_key_verified")
    return credentials.credentials


def get_optional_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security, auto_error=False),
) -> Optional[str]:
    """Get API key without enforcing it (for optional auth).

    Args:
        credentials: HTTP authorization credentials.

    Returns:
        The API key if present and valid, None otherwise.
    """
    if not credentials:
        return None

    if settings.api_key and credentials.credentials == settings.api_key:
        return credentials.credentials

    return None
