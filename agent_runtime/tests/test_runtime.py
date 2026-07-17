import pytest
from agent_runtime.runtime import AgentRuntime
from agent_runtime.interfaces import AdapterInterface, ProviderAdapter
from agent_runtime.runtime_types import SystemContext, Artifact
from agent_runtime.exceptions import RevisionMismatchError

class MockConcurrencyAdapter(AdapterInterface):
    def __init__(self) -> None:
        self.transitions = []
        self.call_count = 0
    
    def sync_context(self) -> SystemContext:
        self.call_count += 1
        return SystemContext(
            process_id="p1", current_state="INIT", revision=self.call_count, 
            allowed_tools=["dummy_tool"], allowed_transitions=["EXECUTING", "VERIFYING", "WAITING", "FAILED"], 
            emergency_stop=False, contract_version="1.0"
        )
        
    def request_transition(self, state: str, revision: int) -> bool:
        if self.call_count == 1 and state == "EXECUTING":
            # Simulate a concurrent modification changing the true revision
            self.call_count += 1
            raise RevisionMismatchError("Revision mismatch")
        self.transitions.append(state)
        return True
        
    def submit_artifact_and_verify(self, artifact: Artifact) -> bool:
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

def test_revision_concurrency_control() -> None:
    """
    Test that Runtime correctly catches RevisionMismatchError,
    discards the plan, resyncs context, and retries.
    """
    adapter = MockConcurrencyAdapter()
    provider = MockProvider()
    runtime = AgentRuntime(adapter, provider)
    
    # Run the runtime
    runtime.run()
    
    # Expected behavior:
    # 1. Sync context (call_count = 1, revision = 1)
    # 2. Plan
    # 3. request_transition("EXECUTING", rev=1) -> throws RevisionMismatchError, call_count becomes 2
    # 4. catch error, clear working memory
    # 5. Loop continues: Sync context (call_count = 3, revision = 3)
    # 6. Plan
    # 7. request_transition("EXECUTING", rev=3) -> Success
    # 8. Exec, Verify, Done
    
    assert adapter.call_count == 3
    assert "EXECUTING" in adapter.transitions

class MockMissingApisAdapter(AdapterInterface):
    def __init__(self) -> None:
        self.call_count = 0

    def sync_context(self) -> SystemContext:
        self.call_count += 1
        return SystemContext(
            process_id="p2", current_state="INIT", revision=1,
            allowed_tools=["dummy_tool"], allowed_transitions=["EXECUTING", "VERIFYING"],
            emergency_stop=False, contract_version="1.0"
        )

    def request_transition(self, state: str, revision: int) -> bool:
        return True

    def submit_artifact_and_verify(self, artifact: Artifact) -> bool:
        return True

    def record_action_intent(self, execution_id: str, action_type: str) -> None:
        pass

    def record_action_receipt(self, execution_id: str, result: str) -> None:
        pass

    def check_receipt_exists(self, execution_id: str) -> bool:
        return False

def test_missing_apis_raises_not_implemented() -> None:
    """
    Test that the runtime raises NotImplementedError when the adapter
    does not implement the required submit_transition_request and wait_for_verifier APIs.
    """
    adapter = MockMissingApisAdapter()
    provider = MockProvider()
    runtime = AgentRuntime(adapter, provider)
    
    with pytest.raises(NotImplementedError) as exc_info:
        runtime.run()
    
    assert "Deferred Dependency: Adapter is missing submit_transition_request() and/or wait_for_verifier() APIs." in str(exc_info.value)

