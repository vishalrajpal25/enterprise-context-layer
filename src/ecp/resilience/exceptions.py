"""Custom exception hierarchy for ECP.

This module defines a structured exception hierarchy that allows for
fine-grained error handling and appropriate HTTP status code mapping.

Exception Hierarchy:
    ECPError (base)
    ├── StoreError (500) - Store operation failures
    │   ├── StoreConnectionError (503) - Cannot connect to store
    │   ├── StoreTimeoutError (504) - Store operation timed out
    │   └── StoreQueryError (500) - Query execution failed
    ├── ResolutionError (400) - Resolution failures
    │   ├── ConceptNotFoundError (404) - Concept not found
    │   ├── AmbiguousConceptError (409) - Multiple interpretations
    │   └── InvalidQueryError (400) - Malformed query
    ├── ValidationError (422) - Validation failures
    │   ├── DataQualityError (422) - Data quality check failed
    │   └── BusinessRuleViolationError (422) - Business rule violated
    └── AuthorizationError (403) - Authorization failures
        ├── InsufficientPermissionsError (403) - User lacks permissions
        └── PolicyDeniedError (403) - Policy explicitly denied access
"""

from typing import Any


class ECPError(Exception):
    """Base exception for all ECP errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        details: Additional error details (dict)
        http_status: Suggested HTTP status code
    """

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
        http_status: int = 500,
    ) -> None:
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.http_status = http_status
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


# Store Errors
class StoreError(ECPError):
    """Base class for store operation errors."""

    def __init__(
        self,
        message: str,
        store_name: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
        http_status: int = 500,
    ) -> None:
        details = details or {}
        details["store"] = store_name
        super().__init__(message, error_code, details, http_status)


class StoreConnectionError(StoreError):
    """Cannot connect to store."""

    def __init__(self, store_name: str, reason: str) -> None:
        super().__init__(
            message=f"Failed to connect to {store_name}: {reason}",
            store_name=store_name,
            error_code="store_connection_error",
            http_status=503,
        )


class StoreTimeoutError(StoreError):
    """Store operation timed out."""

    def __init__(self, store_name: str, operation: str, timeout_seconds: float) -> None:
        super().__init__(
            message=f"{store_name} {operation} timed out after {timeout_seconds}s",
            store_name=store_name,
            error_code="store_timeout_error",
            details={"operation": operation, "timeout_seconds": timeout_seconds},
            http_status=504,
        )


class StoreQueryError(StoreError):
    """Query execution failed."""

    def __init__(self, store_name: str, query: str, reason: str) -> None:
        super().__init__(
            message=f"{store_name} query failed: {reason}",
            store_name=store_name,
            error_code="store_query_error",
            details={"query": query, "reason": reason},
            http_status=500,
        )


# Resolution Errors
class ResolutionError(ECPError):
    """Base class for resolution errors."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, error_code, details, http_status=400)


class ConceptNotFoundError(ResolutionError):
    """Concept not found in knowledge base."""

    def __init__(self, concept: str) -> None:
        super().__init__(
            message=f"Concept not found: {concept}",
            error_code="concept_not_found",
            details={"concept": concept},
        )
        self.http_status = 404


class AmbiguousConceptError(ResolutionError):
    """Multiple interpretations for concept."""

    def __init__(self, concept: str, interpretations: list[str]) -> None:
        super().__init__(
            message=f"Ambiguous concept '{concept}': multiple interpretations found",
            error_code="ambiguous_concept",
            details={"concept": concept, "interpretations": interpretations},
        )
        self.http_status = 409


class InvalidQueryError(ResolutionError):
    """Malformed or invalid query."""

    def __init__(self, query: str, reason: str) -> None:
        super().__init__(
            message=f"Invalid query: {reason}",
            error_code="invalid_query",
            details={"query": query, "reason": reason},
        )


# Validation Errors
class ValidationError(ECPError):
    """Base class for validation errors."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, error_code, details, http_status=422)


class DataQualityError(ValidationError):
    """Data quality check failed."""

    def __init__(self, rule: str, value: Any, threshold: Any) -> None:
        super().__init__(
            message=f"Data quality check failed: {rule}",
            error_code="data_quality_error",
            details={"rule": rule, "value": value, "threshold": threshold},
        )


class BusinessRuleViolationError(ValidationError):
    """Business rule violated."""

    def __init__(self, rule: str, description: str) -> None:
        super().__init__(
            message=f"Business rule violation: {description}",
            error_code="business_rule_violation",
            details={"rule": rule, "description": description},
        )


# Authorization Errors
class AuthorizationError(ECPError):
    """Base class for authorization errors."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, error_code, details, http_status=403)


class InsufficientPermissionsError(AuthorizationError):
    """User lacks required permissions."""

    def __init__(self, required_permission: str, user_role: str) -> None:
        super().__init__(
            message=f"Insufficient permissions: requires '{required_permission}', user has role '{user_role}'",
            error_code="insufficient_permissions",
            details={"required_permission": required_permission, "user_role": user_role},
        )


class PolicyDeniedError(AuthorizationError):
    """Policy explicitly denied access."""

    def __init__(self, policy: str, reason: str) -> None:
        super().__init__(
            message=f"Access denied by policy '{policy}': {reason}",
            error_code="policy_denied",
            details={"policy": policy, "reason": reason},
        )
