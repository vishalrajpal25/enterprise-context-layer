"""FastAPI middleware for observability.

Provides request tracking, logging, and metrics collection.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ecp.observability.logging import bind_request_context, get_logger, unbind_request_context
from ecp.observability.metrics import metrics

logger = get_logger(__name__)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Middleware for request tracking, logging, and metrics.

    For each request:
    - Generates unique request_id
    - Binds request context for structured logging
    - Logs request start/end
    - Collects latency metrics
    - Handles errors
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = request.headers.get("X-Request-ID", f"req_{uuid.uuid4().hex[:16]}")

        # Bind context for structured logging
        bind_request_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )

        # Log request start
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
        )

        # Process request
        start_time = time.time()
        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            # Log request completion
            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_seconds=duration,
            )

            return response

        except Exception as e:
            duration = time.time() - start_time

            # Log error
            logger.error(
                "request_failed",
                error=str(e),
                error_type=type(e).__name__,
                duration_seconds=duration,
                exc_info=True,
            )

            # Record error metric
            metrics.record_error(
                error_type=type(e).__name__,
                component="api",
            )

            raise

        finally:
            # Clear context
            unbind_request_context()
