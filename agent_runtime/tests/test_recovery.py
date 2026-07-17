import pytest
from agent_runtime.recovery import RecoveryManager
from agent_runtime.interfaces import AdapterInterface
from agent_runtime.runtime_types import SystemContext, ExecutionResult, ErrorClassification

class MockRecoveryAdapter(AdapterInterface):
    def __init__(self, receipt_exists: bool = False) -> None:
        self._receipt_exists = receipt_exists
        self.receipts_recorded = []
        
    def sync_context(self): pass
    def request_transition(self, state, revision): pass
    def submit_artifact_and_verify(self, artifact): pass
    def record_action_intent(self, execution_id, action_type): pass
    
    def record_action_receipt(self, execution_id, result):
        self.receipts_recorded.append((execution_id, result))
        
    def check_receipt_exists(self, execution_id: str) -> bool:
        return self._receipt_exists

def test_retry_budget_exhaustion() -> None:
    adapter = MockRecoveryAdapter()
    recovery = RecoveryManager(adapter, max_retries=2)
    
    result = ExecutionResult(execution_id="1", success=False, failed=True, error_type=ErrorClassification.RETRYABLE, receipt_generated=True)
    
    # Retry 1
    assert recovery.handle(result) == "RETRY"
    # Retry 2
    assert recovery.handle(result) == "RETRY"
    # Exhausted -> FAILED
    assert recovery.handle(result) == "FAILED"

def test_crash_recovery_with_receipt() -> None:
    adapter = MockRecoveryAdapter(receipt_exists=True)
    recovery = RecoveryManager(adapter)
    
    # Phase 1 complete, phase 2 incomplete
    result = ExecutionResult(execution_id="2", success=False, failed=True, receipt_generated=False)
    
    # Handle should recover because receipt exists
    state = recovery.handle(result)
    assert state is None
    assert not result.failed
    assert result.receipt_generated
    assert len(adapter.receipts_recorded) == 1

def test_wait_required() -> None:
    adapter = MockRecoveryAdapter()
    recovery = RecoveryManager(adapter)
    
    result = ExecutionResult(execution_id="3", success=False, failed=True, error_type=ErrorClassification.WAIT_REQUIRED, receipt_generated=True)
    assert recovery.handle(result) == "WAITING"

def test_fatal_error() -> None:
    adapter = MockRecoveryAdapter()
    recovery = RecoveryManager(adapter)
    
    result = ExecutionResult(execution_id="4", success=False, failed=True, error_type=ErrorClassification.FATAL, receipt_generated=True)
    assert recovery.handle(result) == "FAILED"


from agent_runtime.exceptions import RecoveryError, RevisionMismatchError
from agent_runtime.runtime import AgentRuntime
from agent_runtime.interfaces import ProviderAdapter

def test_unknown_receipt_raises_recovery_error() -> None:
    adapter = MockRecoveryAdapter(receipt_exists=False)
    recovery = RecoveryManager(adapter)
    
    # Intent exists, but receipt not generated and check_receipt_exists returns False
    result = ExecutionResult(execution_id="5", success=False, failed=True, receipt_generated=False)
    
    with pytest.raises(RecoveryError) as exc_info:
        recovery.handle(result)
    assert "Unknown receipt" in str(exc_info.value)


class MockAlwaysMismatchAdapter(AdapterInterface):
    def sync_context(self) -> SystemContext:
        return SystemContext(
            process_id="p1", current_state="INIT", revision=1, 
            allowed_tools=["dummy_tool"], allowed_transitions=["EXECUTING"], 
            emergency_stop=False, contract_version="1.0"
        )
    def request_transition(self, state: str, revision: int) -> bool:
        raise RevisionMismatchError("Transient revision mismatch")
    def submit_artifact_and_verify(self, artifact) -> bool:
        return True
    def record_action_intent(self, execution_id, action_type) -> None:
        pass
    def record_action_receipt(self, execution_id, result) -> None:
        pass
    def check_receipt_exists(self, execution_id) -> bool:
        return False

class MockProvider(ProviderAdapter):
    def generate_response(self, prompt: str) -> str:
        return "{'tool': 'dummy_tool'}"

def test_revision_mismatch_aborts_execution() -> None:
    adapter = MockAlwaysMismatchAdapter()
    provider = MockProvider()
    runtime = AgentRuntime(adapter, provider, max_revision_retries=2)
    
    with pytest.raises(RevisionMismatchError):
        runtime.run()


