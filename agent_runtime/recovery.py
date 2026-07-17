"""
RecoveryManager module for the Layer 3 Agent Runtime.

Handles execution failures and enforces crash recovery policies.
"""

import time
from typing import Optional
from .runtime_types import ExecutionResult, ErrorClassification
from .interfaces import AdapterInterface

__all__ = ["RecoveryManager"]

# TODO(runtime): Implement exponential backoff for retry wait periods.
# TODO(test): Verify recovery handling in test_recovery.py.


class RecoveryManager:
    """Manages failure recovery and handles crash recovery logic."""

    def __init__(self, adapter: AdapterInterface, max_retries: int = 3) -> None:
        self.adapter: AdapterInterface = adapter
        self.max_retries: int = max_retries
        self.retry_budget: int = max_retries

    def handle(self, result: ExecutionResult) -> Optional[str]:
        """
        Handles execution failures based on error classification.
        Returns the requested transition state (if any) such as "WAITING" or "FAILED".
        Returns None if a retry was successfully performed or scheduled.
        """
        if not result.failed:
            return None

        # Crash Recovery logic for Two-Phase Action Records
        # Find Intent without Receipt
        if result.execution_id and not result.receipt_generated:
            receipt_exists = self.adapter.check_receipt_exists(result.execution_id)
            if receipt_exists:
                self.adapter.record_action_receipt(result.execution_id, "success_recovered")
                result.receipt_generated = True
                result.failed = False
                return None # Recovered, no transition needed
            else:
                from .exceptions import RecoveryError
                raise RecoveryError("Unknown receipt: action intent exists but no receipt was found. Manual verification required.") 

        if result.error_type == ErrorClassification.RETRYABLE:
            if self.retry_budget > 0:
                self.retry_budget -= 1
                self._backoff_retry()
                # A real implementation would trigger executor again here or queue the plan step
                return "RETRY" # Special internal state indicating retry allowed
            else:
                return "FAILED"

        elif result.error_type == ErrorClassification.WAIT_REQUIRED:
            return "WAITING"

        elif result.error_type == ErrorClassification.FATAL:
            return "FAILED"

        return "FAILED" # Default fallback

    def _backoff_retry(self) -> None:
        """Simulates a backoff sleep (mocked for testing)."""
        time.sleep(0.01)

    def reset_budget(self) -> None:
        self.retry_budget = self.max_retries

