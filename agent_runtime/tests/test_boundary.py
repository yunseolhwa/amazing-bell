import pytest
from agent_runtime.runtime import AgentRuntime
from agent_runtime.interfaces import AdapterInterface, ProviderAdapter
from agent_runtime.runtime_types import SystemContext, Artifact

class MockAdapter(AdapterInterface):
    def __init__(self) -> None:
        self.transitions = []
        self.artifacts_submitted = []
    
    def sync_context(self) -> SystemContext:
        return SystemContext(
            process_id="p1", current_state="INIT", revision=1, 
            allowed_tools=["dummy_tool"], allowed_transitions=["EXECUTING", "VERIFYING", "WAITING", "FAILED"], 
            emergency_stop=False, contract_version="1.0"
        )
        
    def request_transition(self, state: str, revision: int) -> bool:
        self.transitions.append(state)
        return True
        
    def submit_artifact_and_verify(self, artifact: Artifact) -> bool:
        self.artifacts_submitted.append(artifact)
        return True
        
    def record_action_intent(self, execution_id: str, action_type: str) -> None:
        pass
        
    def record_action_receipt(self, execution_id: str, result: str) -> None:
        pass
        
    def check_receipt_exists(self, execution_id: str) -> bool:
        return False

    def submit_transition_request(self) -> None:
        pass

    def wait_for_verifier(self) -> None:
        pass

class MockProvider(ProviderAdapter):
    def generate_response(self, prompt: str) -> str:
        return "{'tool': 'dummy_tool'}"

def test_runtime_uses_adapter_strictly() -> None:
    """
    Test that Runtime doesn't have methods to write to DB,
    fake completions or bypass adapter.
    """
    adapter = MockAdapter()
    provider = MockProvider()
    runtime = AgentRuntime(adapter, provider)
    
    # Boundary: No DB write method
    assert not hasattr(runtime, 'direct_db_write')
    assert not hasattr(runtime, 'kernel')
    assert not hasattr(runtime, 'force_complete')
    
    # Run a simple iteration
    runtime.run()
    
    # Verify it used the adapter properly
    assert "EXECUTING" in adapter.transitions
    assert "VERIFYING" in adapter.transitions
    assert len(adapter.artifacts_submitted) > 0

    # Runtime should rely entirely on adapter for completions
    assert "COMPLETED" not in adapter.transitions # Kernel does completion!


from agent_runtime.exceptions import AccessError, RuntimeContractViolation
from agent_runtime.contracts import RuntimeContractValidator

class Test_Runtime_CannotImportKernel:
    def test_import_blocked(self):
        with pytest.raises(ImportError) as exc_info:
            import kernel_module
        assert "blocked" in str(exc_info.value)

class Test_Runtime_CannotUseSQLite:
    def test_sqlite3_import_blocked(self):
        with pytest.raises(AccessError) as exc_info:
            import sqlite3
        assert "blocked" in str(exc_info.value)

class Test_Runtime_CannotSetCompleted:
    def test_completed_state_forbidden(self):
        with pytest.raises(RuntimeContractViolation) as exc_info:
            RuntimeContractValidator.validate_state("COMPLETED")
        assert "forbidden" in str(exc_info.value)
        
        with pytest.raises(RuntimeContractViolation) as exc_info2:
            RuntimeContractValidator.validate_transition("INIT", "COMPLETED")
        assert "forbidden" in str(exc_info2.value)

class Test_Runtime_CannotCallVerifier:
    def test_verifier_import_blocked(self):
        with pytest.raises(AccessError) as exc_info:
            import verifier
        assert "blocked" in str(exc_info.value)

class Test_Runtime_CannotBypassAdapter:
    def test_bypass_raises_violation(self):
        adapter = MockAdapter()
        provider = MockProvider()
        runtime = AgentRuntime(adapter, provider)
        with pytest.raises(RuntimeContractViolation) as exc_info:
            runtime.update_state_directly("EXECUTING")
        assert "outside of the adapter" in str(exc_info.value)


