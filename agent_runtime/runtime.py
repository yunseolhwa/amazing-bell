"""
AgentRuntime module for the Layer 3 Agent Runtime.

Implements the main execution loop, context synchronization, action coordination,
and error recovery.
"""

from typing import Optional
from .interfaces import AdapterInterface, ProviderAdapter
from .exceptions import RevisionMismatchError
from .runtime_types import SystemContext
from .contracts import RuntimeContractValidator
from .planner import Planner
from .executor import Executor
from .recovery import RecoveryManager
from .memory import AgentMemory

__all__ = ["AgentRuntime"]

# TODO(runtime): Implement state persistence between iterations of the main loop.
# TODO(test): Verify main loop execution flow in test_runtime.py.


class AgentRuntime:
    """The Layer 3 Agent Runtime orchestrating planning, execution, and recovery."""

    def __init__(self, adapter: AdapterInterface, provider: ProviderAdapter, max_revision_retries: int = 3) -> None:
        self.adapter: AdapterInterface = adapter
        self.planner: Planner = Planner(provider)
        self.executor: Executor = Executor(adapter)
        self.recovery: RecoveryManager = RecoveryManager(adapter)
        self.memory: Optional[AgentMemory] = None
        self.max_revision_retries: int = max_revision_retries

    def run(self) -> None:
        """Main Loop for the Agent Runtime."""
        revision_retries = 0
        while True:
            # 1. Context Sync
            context: SystemContext = self.adapter.sync_context()
            
            if self.memory is None:
                # Assuming audit logs would be passed from adapter or kernel in real world
                self.memory = AgentMemory(context, kernel_logs=[])
            else:
                self.memory.short_memory.update_context(context)

            if context.emergency_stop:
                self.enter_waiting()
                break

            # 2. Revision Concurrency Check loop
            try:
                # 3. Plan 생성
                plan = self.planner.create_plan(context)
                self.memory.working_memory.set_plan(plan)

                # Attempt to transition to executing/verifying
                # This throws RevisionMismatchError if someone else modified process
                RuntimeContractValidator.validate_transition(context.current_state, "EXECUTING")
                self.adapter.request_transition(state="EXECUTING", revision=context.revision)

                # 4. Tool 실행
                result = self.executor.execute(plan)
                self.memory.working_memory.add_result(result)

                # 5. Verification 대기
                if result.requires_verification and result.artifact:
                    # Check if the adapter exposes the new transition and verification APIs
                    if not hasattr(self.adapter, "submit_transition_request") or not hasattr(self.adapter, "wait_for_verifier"):
                        # TODO(runtime): Deferred Dependency - submit_transition_request and wait_for_verifier are not yet exposed.
                        # Stop implementation here per the Interface Change Policy and raise an error.
                        raise NotImplementedError(
                            "Deferred Dependency: Adapter is missing submit_transition_request() and/or wait_for_verifier() APIs."
                        )
                    
                    # If they were present, we would call:
                    # self.adapter.submit_transition_request(...)
                    # self.adapter.wait_for_verifier(...)
                    
                    # Request transition to VERIFYING (legacy fallback for tests)
                    RuntimeContractValidator.validate_transition(context.current_state, "VERIFYING")
                    self.adapter.request_transition(state="VERIFYING", revision=context.revision)
                    self.adapter.submit_artifact_and_verify(result.artifact)
                    
                    # Once verified by verifier, Kernel will update state to Completed
                    # Runtime doesn't force complete.

                # 6. Recovery 처리
                if result.failed:
                    self.memory.working_memory.set_error(str(result.error_message))
                    recovery_state = self.recovery.handle(result)
                    
                    if recovery_state:
                        # Request transition to WAITING or FAILED based on recovery policy
                        RuntimeContractValidator.validate_transition(context.current_state, recovery_state)
                        self.adapter.request_transition(state=recovery_state, revision=context.revision)
                        if recovery_state == "FAILED":
                            break
                        elif recovery_state == "WAITING":
                            self.enter_waiting()
                            break

                # For testing/skeleton: break out of the infinite loop if successful
                if result.success:
                    break

            except RevisionMismatchError as e:
                # Revision Concurrency Control: Mismatch -> discard plan -> sync -> replan
                revision_retries += 1
                if revision_retries > self.max_revision_retries:
                    raise e
                self.memory.working_memory.clear()
                continue

    def enter_waiting(self) -> None:
        """Enters a waiting state (e.g., for human approval)."""
        pass

    def update_state_directly(self, state: str) -> None:
        """
        Attempts to update/transition state directly bypassing the adapter.
        Always raises RuntimeContractViolation to enforce adapter boundaries.
        """
        from .exceptions import RuntimeContractViolation
        raise RuntimeContractViolation("Cannot perform state transitions or updates outside of the adapter.")


