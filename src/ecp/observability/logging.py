"""Structured logging with request IDs and contextual information.

This module provides production-grade structured logging using structlog.
All logs are output in JSON format for easy parsing and analysis.

Usage:
    from ecp.observability import get_logger, setup_logging

    # Initialize logging (done once at app startup)
    setup_logging()

    # Get a logger
    logger = get_logger(__name__)

    # Log with context
    logger.info("resolving_concept", concept="revenue", user_id="u_123")
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor


def add_app_context(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log entries."""
    event_dict["app"] = "ecp"
    event_dict["service"] = "resolution-api"
    return event_dict


def setup_logging(log_level: str = "INFO", json_logs: bool = True) -> None:
    """Configure structured logging for the application.

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: If True, output JSON format; if False, use console format
    """
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Build processor chain
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        add_app_context,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        # Production: JSON output
        processors.append(structlog.processors.JSONRenderer())
    else:
        # Development: Pretty console output
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=True),
        ])

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


# Context management for request-scoped logging
def bind_request_context(**kwargs: Any) -> None:
    """Bind context to current request/task.

    This should be called at the beginning of each request with:
    - request_id: Unique request identifier
    - user_id: User making the request
    - Any other relevant context

    Example:
        bind_request_context(request_id="req_123", user_id="u_456")
    """
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_request_context() -> None:
    """Clear request context."""
    structlog.contextvars.clear_contextvars()
