"""
Agent Runtime Layer 3 Package.

This package provides the core L3 Agent Runtime implementation, interfaces,
contracts, types, and exceptions.
"""

import sys
from .runtime import AgentRuntime
from .interfaces import AdapterInterface, ProviderAdapter
from .runtime_types import SystemContext, Artifact, ExecutionResult, Plan, ErrorClassification
from .exceptions import RevisionMismatchError, AccessError, RuntimeContractViolation, RecoveryError
from .contracts import RuntimeContractValidator

class ForbiddenModuleBlocker:
    """A sys.meta_path hook that intercepts and blocks prohibited imports."""
    def find_spec(self, fullname, path, target=None):
        if fullname == "sqlite3" or fullname.startswith("sqlite3.") or fullname.startswith("verifier") or fullname.startswith("state_storage"):
            raise AccessError(f"Access to forbidden module '{fullname}' is blocked.")
        if fullname.startswith("kernel"):
            raise ImportError(f"Import of forbidden module '{fullname}' is blocked.")
        return None

# Register the hook if not already registered
if not any(isinstance(hook, ForbiddenModuleBlocker) for hook in sys.meta_path):
    sys.meta_path.insert(0, ForbiddenModuleBlocker())

__all__ = [
    "AgentRuntime",
    "AdapterInterface",
    "ProviderAdapter",
    "SystemContext",
    "Artifact",
    "ExecutionResult",
    "Plan",
    "ErrorClassification",
    "RevisionMismatchError",
    "RuntimeContractViolation",
    "AccessError",
    "RecoveryError",
    "RuntimeContractValidator",
    "ForbiddenModuleBlocker",
]

# TODO(runtime): Add initialization checks for environment variables and platform compatibility.
# TODO(test): Verify package initialization and public exports.


