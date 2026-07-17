"""
Exceptions for the Layer 3 Agent Runtime.

This module contains custom exceptions used across the runtime, including
concurrency control errors.
"""

__all__ = [
    "RevisionMismatchError",
    "RuntimeContractViolation",
    "AccessError",
    "RecoveryError",
]

# TODO(contract): Add more specific error types for validation or transition failures.
# TODO(test): Verify exception behavior in tests.


class RevisionMismatchError(Exception):
    """
    Raised when a requested transition fails due to a revision mismatch
    with the true state in the kernel.
    """
    pass


class RuntimeContractViolation(Exception):
    """
    Raised when a state transition or logic contract is violated.
    """
    pass


class AccessError(Exception):
    """
    Raised when a forbidden resource or module is accessed/imported.
    """
    pass


class RecoveryError(Exception):
    """
    Raised when recovery fails, is invalid, or requires manual intervention.
    """
    pass

