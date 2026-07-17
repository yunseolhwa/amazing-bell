"""
Runtime types and structures for the Layer 3 Agent Runtime.

This module defines data structures, contexts, execution results, plans,
and error classifications.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

__all__ = [
    "ErrorClassification",
    "SystemContext",
    "Artifact",
    "ExecutionResult",
    "Plan",
]

# TODO(runtime): Add configuration loading and serialization helpers for these types.
# TODO(test): Add unit tests for runtime types serialization.


class ErrorClassification(Enum):
    RETRYABLE = "RETRYABLE"
    WAIT_REQUIRED = "WAIT_REQUIRED"
    FATAL = "FATAL"

@dataclass
class SystemContext:
    process_id: str
    current_state: str
    revision: int
    allowed_tools: List[str]
    allowed_transitions: List[str]
    emergency_stop: bool
    contract_version: str

@dataclass
class Artifact:
    content: str
    type: str

@dataclass
class ExecutionResult:
    execution_id: str
    success: bool
    artifact: Optional[Artifact] = None
    requires_verification: bool = False
    failed: bool = False
    error_type: Optional[ErrorClassification] = None
    error_message: Optional[str] = None
    receipt_generated: bool = False

@dataclass
class Plan:
    steps: List[Dict[str, Any]]
