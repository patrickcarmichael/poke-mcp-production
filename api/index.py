"""Vercel serverless function handler for MCP server."""
from fastapi import FastAPI, Depends, status as http_status
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

from src.config import settings
from src.logger import configure_logging, get_logger
from src.auth import verify_api_key
from src.middleware import (
    setup_cors_middleware,
    RateLimitMiddleware,
    RequestLoggingMiddleware,
)
from src.monitoring import metrics_middleware, server_info

# Configure logging
configure_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.server_name,
    version=settings.server_version,
    description="Production-ready Poke MCP Server with authentication and monitoring",
)

# Setup middleware
setup_cors_middleware(app)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    requests=settings.rate_limit_requests,
    window=settings.rate_limit_window,
)
app.middleware("http")(metrics_middleware)

# Set server info
server_info.info(
    {
        "name": settings.server_name,
        "version": settings.server_version,
        "environment": settings.environment,
    }
)

logger.info(
    "app_initialized",
    name=settings.server_name,
    version=settings.server_version,
    environment=settings.environment,
)


@app.get("/")
async def root() -> dict:
    """Root endpoint with server information."""
    return {
        "name": settings.server_name,
        "version": settings.server_version,
        "status": "running",
        "environment": settings.environment,
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "mcp": "/mcp",
        },
    }


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "server": settings.server_name,
        "version": settings.server_version,
    }


@app.get("/metrics")
async def metrics() -> Response:
    """Prometheus metrics endpoint."""
    if not settings.enable_metrics:
        return JSONResponse(
            status_code=http_status.HTTP_404_NOT_FOUND,
            content={"error": "Metrics disabled"},
        )
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/mcp")
async def mcp_endpoint(
    request_data: dict,
    api_key: str = Depends(verify_api_key),
) -> dict:
    """MCP protocol endpoint with authentication.
    
    This endpoint handles MCP tool calls with proper authentication.
    In a production environment, this would integrate with the MCP server
    to execute tool calls.
    
    Args:
        request_data: The MCP request payload
        api_key: Verified API key from authorization header
    
    Returns:
        MCP response
    """
    logger.info("mcp_request_received", request=request_data)
    
    # TODO: Integrate with actual MCP server tool execution
    # For now, return a placeholder response
    return {
        "status": "success",
        "message": "MCP endpoint - integrate with actual tool execution",
        "request": request_data,
    }


@app.get("/status")
async def status(api_key: str = Depends(verify_api_key)) -> dict:
    """Protected status endpoint requiring authentication."""
    return {
        "status": "authenticated",
        "server": settings.server_name,
        "version": settings.server_version,
        "environment": settings.environment,
        "features": {
            "authentication": True,
            "rate_limiting": settings.rate_limit_enabled,
            "metrics": settings.enable_metrics,
            "logging": True,
        },
    }


# Vercel serverless function handler
handler = app
