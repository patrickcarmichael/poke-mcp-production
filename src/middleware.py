"""Custom middleware for request processing."""
import time
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from src.config import settings
from src.logger import get_logger
import structlog

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, requests: int = 100, window: int = 60):
        super().__init__(app)
        self.requests = requests
        self.window = window
        self.clients = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process rate limiting."""
        if not settings.rate_limit_enabled:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Clean old entries
        self.clients = {
            ip: timestamps
            for ip, timestamps in self.clients.items()
            if any(t > current_time - self.window for t in timestamps)
        }

        # Check rate limit
        if client_ip in self.clients:
            timestamps = [
                t for t in self.clients[client_ip] if t > current_time - self.window
            ]
            if len(timestamps) >= self.requests:
                logger.warning("rate_limit_exceeded", client_ip=client_ip)
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "detail": f"Maximum {self.requests} requests per {self.window} seconds",
                    },
                )
            timestamps.append(current_time)
            self.clients[client_ip] = timestamps
        else:
            self.clients[client_ip] = [current_time]

        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured request/response logging."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response details."""
        request_id = str(time.time())
        structlog.contextvars.bind_contextvars(request_id=request_id)

        logger.info(
            "request_started",
            method=request.method,
            url=str(request.url),
            client=request.client.host if request.client else None,
        )

        start_time = time.time()
        try:
            response = await call_next(request)
            duration = time.time() - start_time

            logger.info(
                "request_completed",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                duration=duration,
            )

            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "request_failed",
                method=request.method,
                url=str(request.url),
                error=str(e),
                duration=duration,
            )
            raise
        finally:
            structlog.contextvars.unbind_contextvars("request_id")


def setup_cors_middleware(app) -> None:
    """Setup CORS middleware.

    Args:
        app: FastAPI application instance.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
