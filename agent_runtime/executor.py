"""
Executor module for the Layer 3 Agent Runtime.

Handles execution of plans and enforces the Two-Phase Action Record.
"""

import uuid
from typing import Optional
from .runtime_types import Plan, ExecutionResult, Artifact, ErrorClassification
from .interfaces import AdapterInterface

__all__ = ["Executor"]

# TODO(runtime): Implement support for routing multi-step plans.
# TODO(test): Verify executor logic under different execution flows.


class Executor:
    """Executes planned actions and records action intents/receipts."""

    def __init__(self, adapter: AdapterInterface) -> None:
        self.adapter: AdapterInterface = adapter

    def execute(self, plan: Plan) -> ExecutionResult:
        """
        Executes a plan. 
        Enforces Two-Phase Action Record for external effects.
        """
        if not plan.steps:
            return ExecutionResult(execution_id="", success=True)
            
        # Simplified execution for skeleton
        step = plan.steps[0]
        execution_id = str(uuid.uuid4())
        
        try:
            # Phase 1: Action Intent
            self.adapter.record_action_intent(execution_id, step.get("action", "unknown"))
            
            # Simulate Tool Execution (This would normally call the tool_router)
            # tool_router.route(step)
            
            # Phase 2: Action Receipt
            self.adapter.record_action_receipt(execution_id, "success")
            
            # Generate Artifact
            artifact = Artifact(content="execution_result_data", type="result")
            
            return ExecutionResult(
                execution_id=execution_id,
                success=True,
                artifact=artifact,
                requires_verification=True,
                receipt_generated=True
            )
            
        except Exception as e:
            # Handle failure
            return ExecutionResult(
                execution_id=execution_id,
                success=False,
                failed=True,
                error_type=ErrorClassification.FATAL, # For simplicity
                error_message=str(e),
                receipt_generated=False
            )

