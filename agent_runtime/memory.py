"""
Memory components for the Layer 3 Agent Runtime.

Provides short-term memory, working memory, and read-only audit history.
"""

from typing import List, Dict, Any, Optional
from .runtime_types import SystemContext, Plan

__all__ = ["ShortMemory", "WorkingMemory", "AuditHistory", "AgentMemory"]

# TODO(memory): Add periodic persistence of working memory to external storage.
# TODO(test): Verify memory isolation in test_memory.py.


class ShortMemory:
    """Current Task Context."""
    def __init__(self, context: SystemContext) -> None:
        self._context: SystemContext = context

    @property
    def context(self) -> SystemContext:
        return self._context

    def update_context(self, context: SystemContext) -> None:
        self._context = context

class WorkingMemory:
    """Plan, Intermediate Results, Compressed Error."""
    def __init__(self) -> None:
        self.plan: Optional[Plan] = None
        self.intermediate_results: List[Any] = []
        self.compressed_error: Optional[str] = None

    def set_plan(self, plan: Plan) -> None:
        self.plan = plan

    def add_result(self, result: Any) -> None:
        self.intermediate_results.append(result)

    def set_error(self, error: str) -> None:
        self.compressed_error = error

    def clear(self) -> None:
        self.plan = None
        self.intermediate_results.clear()
        self.compressed_error = None

class AuditHistory:
    """Read Only, Kernel Truth. Cannot be merged into Working Memory or Short Memory directly."""
    def __init__(self, kernel_truth_logs: List[str]) -> None:
        self._logs: tuple = tuple(kernel_truth_logs) # Immutable

    @property
    def logs(self) -> tuple:
        return self._logs

class AgentMemory:
    """
    Main memory container.
    Enforces isolation: Audit history is read-only and separate.
    """
    def __init__(self, context: SystemContext, kernel_logs: List[str]) -> None:
        self.short_memory: ShortMemory = ShortMemory(context)
        self.working_memory: WorkingMemory = WorkingMemory()
        self._audit_history: AuditHistory = AuditHistory(kernel_logs)

    @property
    def audit_history(self) -> AuditHistory:
        return self._audit_history

