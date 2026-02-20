"""Retry logic with exponential backoff for transient failures.

This module provides retry decorators and utilities for handling transient
failures in store operations and external API calls.

Key Features:
- Exponential backoff with jitter
- Configurable max retries and timeouts
- Automatic classification of retryable vs non-retryable errors
- Metrics and logging integration

Usage:
    from ecp.resilience import with_retry

    @with_retry(store_name="neo4j")
    async def query_graph(query: str):
        # This will automatically retry on transient errors
        return await graph_db.run(query)
"""

import asyncio
from functools import wraps
from typing import Any, Callable, TypeVar

from tenacity import (
    RetryError,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from ecp.observability import get_logger, metrics

logger = get_logger(__name__)

# Type variable for decorated functions
F = TypeVar("F", bound=Callable[..., Any])


# Classification of errors
RETRYABLE_EXCEPTIONS = (
    # Network/connection errors
    ConnectionError,
    ConnectionRefusedError,
    ConnectionResetError,
    TimeoutError,
    asyncio.TimeoutError,
    # Common HTTP errors (if using httpx/requests)
    # httpx.ConnectError,
    # httpx.TimeoutException,
)

NON_RETRYABLE_EXCEPTIONS = (
    # Authorization/authentication errors
    PermissionError,
    # Validation errors
    ValueError,
    TypeError,
    KeyError,
    AttributeError,
)


def is_retryable(exception: BaseException) -> bool:
    """Determine if an exception is retryable.

    Retryable errors:
    - Connection errors
    - Timeouts
    - Transient network failures
    - 5xx HTTP errors (if applicable)

    Non-retryable errors:
    - 4xx HTTP errors (client errors)
    - Authentication/authorization failures
    - Validation errors
    - Programming errors (TypeError, AttributeError, etc.)

    Args:
        exception: The exception to classify

    Returns:
        True if retryable, False otherwise
    """
    # Check if explicitly non-retryable
    if isinstance(exception, NON_RETRYABLE_EXCEPTIONS):
        return False

    # Check if explicitly retryable
    if isinstance(exception, RETRYABLE_EXCEPTIONS):
        return True

    # Check for store-specific errors
    # Import here to avoid circular dependency
    try:
        from ecp.resilience.exceptions import (
            AuthorizationError,
            StoreConnectionError,
            StoreTimeoutError,
            ValidationError,
        )

        # Store connection and timeout errors are retryable
        if isinstance(exception, (StoreConnectionError, StoreTimeoutError)):
            return True

        # Authorization and validation errors are not retryable
        if isinstance(exception, (AuthorizationError, ValidationError)):
            return False
    except ImportError:
        pass

    # Check HTTP status codes if available
    if hasattr(exception, "status_code"):
        status = exception.status_code
        # 5xx errors are retryable (server errors)
        if 500 <= status < 600:
            return True
        # 4xx errors are not retryable (client errors)
        if 400 <= status < 500:
            return False

    # Check for specific error messages that indicate transient failures
    error_msg = str(exception).lower()
    transient_indicators = [
        "timeout",
        "connection",
        "temporary",
        "unavailable",
        "overloaded",
        "too many requests",
        "rate limit",
    ]

    if any(indicator in error_msg for indicator in transient_indicators):
        return True

    # Default: don't retry unknown exceptions
    return False


def retry_on_transient_error(exception: BaseException) -> bool:
    """Tenacity predicate for retrying on transient errors.

    Args:
        exception: The exception that occurred

    Returns:
        True if should retry, False otherwise
    """
    should_retry = is_retryable(exception)

    if should_retry:
        logger.debug(
            "retryable_error_detected",
            error=str(exception),
            error_type=type(exception).__name__,
        )
    else:
        logger.debug(
            "non_retryable_error_detected",
            error=str(exception),
            error_type=type(exception).__name__,
        )

    return should_retry


def with_retry(
    max_attempts: int = 3,
    min_wait: float = 1.0,
    max_wait: float = 10.0,
    store_name: str | None = None,
) -> Callable[[F], F]:
    """Decorator to add retry logic to async functions.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        min_wait: Minimum wait time between retries in seconds (default: 1.0)
        max_wait: Maximum wait time between retries in seconds (default: 10.0)
        store_name: Optional store name for metrics tracking

    Returns:
        Decorated function with retry logic

    Example:
        @with_retry(max_attempts=3, store_name="neo4j")
        async def query_graph(query: str):
            return await graph_db.run(query)
    """

    def decorator(func: F) -> F:
        # Create retry decorator
        retry_decorator = retry(
            retry=retry_if_exception(retry_on_transient_error),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential_jitter(
                initial=min_wait,
                max=max_wait,
                jitter=min_wait * 0.5,  # Add jitter to avoid thundering herd
            ),
            reraise=True,
        )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            last_exception = None

            # Apply tenacity retry
            try:
                @retry_decorator
                async def _execute() -> Any:
                    nonlocal attempt, last_exception
                    attempt += 1

                    try:
                        logger.debug(
                            "retry_attempt",
                            function=func.__name__,
                            attempt=attempt,
                            max_attempts=max_attempts,
                            store=store_name,
                        )

                        result = await func(*args, **kwargs)
                        return result

                    except Exception as e:
                        last_exception = e

                        if attempt < max_attempts and is_retryable(e):
                            logger.warning(
                                "retry_attempt_failed",
                                function=func.__name__,
                                attempt=attempt,
                                max_attempts=max_attempts,
                                error=str(e),
                                error_type=type(e).__name__,
                                will_retry=True,
                                store=store_name,
                            )

                            # Record retry metric
                            if store_name:
                                metrics.record_store_query(
                                    store=store_name,
                                    duration=0.0,
                                    error=f"retry_{type(e).__name__}",
                                )
                        else:
                            logger.error(
                                "retry_exhausted" if attempt >= max_attempts else "non_retryable_error",
                                function=func.__name__,
                                attempt=attempt,
                                max_attempts=max_attempts,
                                error=str(e),
                                error_type=type(e).__name__,
                                store=store_name,
                            )

                        raise

                return await _execute()

            except RetryError as e:
                # Tenacity exhausted retries, raise original exception
                logger.error(
                    "all_retries_failed",
                    function=func.__name__,
                    attempts=attempt,
                    last_error=str(last_exception),
                    store=store_name,
                )

                if last_exception:
                    raise last_exception from e
                raise

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            # For sync functions, just call directly (no retry for sync)
            # In production, all I/O should be async
            logger.warning(
                "sync_function_no_retry",
                function=func.__name__,
                message="Retry logic only supports async functions",
            )
            return func(*args, **kwargs)

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator
