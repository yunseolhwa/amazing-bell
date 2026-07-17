"""
Interfaces for the Layer 3 Agent Runtime.

This module defines the abstract base classes (ABCs) that must be implemented
by external adapters (e.g. Kernel Adapter, LLM Provider Adapter).
"""

import abc
from .runtime_types import SystemContext, Artifact

__all__ = ["ProviderAdapter", "AdapterInterface"]

# TODO(contract): Define asynchronous variants for adapter and provider interfaces.
# TODO(test): Verify interface definitions via test suite.


class ProviderAdapter(abc.ABC):
    """Abstract base class for LLM/provider communication."""

    @abc.abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generates a text response from the provider based on a prompt."""
        pass

class AdapterInterface(abc.ABC):
    """Abstract base class for interacting with the orchestration/kernel environment."""

    @abc.abstractmethod
    def sync_context(self) -> SystemContext:
        """Retrieves and synchronizes the current SystemContext."""
        pass
        
    @abc.abstractmethod
    def request_transition(self, state: str, revision: int) -> bool:
        """
        Requests a state transition.
        Throws RevisionMismatchError if revision doesn't match kernel truth.
        """
        pass
        
    @abc.abstractmethod
    def submit_artifact_and_verify(self, artifact: Artifact) -> bool:
        """Submits an artifact to the environment for verification."""
        pass
        
    @abc.abstractmethod
    def record_action_intent(self, execution_id: str, action_type: str) -> None:
        """Records the intent to execute an action (Phase 1)."""
        pass
        
    @abc.abstractmethod
    def record_action_receipt(self, execution_id: str, result: str) -> None:
        """Records the receipt/result of an action execution (Phase 2)."""
        pass
        
    @abc.abstractmethod
    def check_receipt_exists(self, execution_id: str) -> bool:
        """Checks if an action receipt exists for the given execution ID."""
        pass
