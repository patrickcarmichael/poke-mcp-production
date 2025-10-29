"""Monitoring and metrics collection using Prometheus."""
from prometheus_client import Counter, Histogram, Gauge, Info
import time
from typing import Callable
from fastapi import Request, Response
from src.logger import get_logger

logger = get_logger(__name__)

# Metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

mcp_tool_calls_total = Counter(
    "mcp_tool_calls_total",
    "Total MCP tool calls",
    ["tool_name", "status"],
)

mcp_tool_duration_seconds = Histogram(
    "mcp_tool_duration_seconds",
    "MCP tool execution duration in seconds",
    ["tool_name"],
)

pokeapi_requests_total = Counter(
    "pokeapi_requests_total",
    "Total PokeAPI requests",
    ["endpoint", "status"],
)

active_connections = Gauge(
    "active_connections",
    "Number of active connections",
)

server_info = Info(
    "server_info",
    "Server information",
)


async def metrics_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware to collect HTTP request metrics.

    Args:
        request: The incoming request.
        call_next: The next middleware/route handler.

    Returns:
        The response.
    """
    start_time = time.time()
    active_connections.inc()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        # Record metrics
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        return response
    finally:
        active_connections.dec()


def record_tool_call(tool_name: str, duration: float, status: str) -> None:
    """Record MCP tool call metrics.

    Args:
        tool_name: Name of the tool called.
        duration: Execution duration in seconds.
        status: Status of the call (success/error).
    """
    mcp_tool_calls_total.labels(tool_name=tool_name, status=status).inc()
    mcp_tool_duration_seconds.labels(tool_name=tool_name).observe(duration)
    logger.info(
        "tool_call_recorded",
        tool_name=tool_name,
        duration=duration,
        status=status,
    )


def record_pokeapi_request(endpoint: str, status: int) -> None:
    """Record PokeAPI request metrics.

    Args:
        endpoint: The API endpoint called.
        status: HTTP status code.
    """
    pokeapi_requests_total.labels(endpoint=endpoint, status=status).inc()
