import pytest
from agent_runtime.memory import AgentMemory
from agent_runtime.runtime_types import SystemContext

def test_memory_isolation() -> None:
    context = SystemContext(
        process_id="p1", current_state="INIT", revision=1, 
        allowed_tools=[], allowed_transitions=[], emergency_stop=False, contract_version="1.0"
    )
    
    kernel_logs = ["log1", "log2"]
    memory = AgentMemory(context, kernel_logs)
    
    # Verify Audit History is read only
    assert isinstance(memory.audit_history.logs, tuple)
    assert "log1" in memory.audit_history.logs
    
    with pytest.raises(AttributeError):
        # Should not be able to append to logs directly
        memory.audit_history.logs.append("fake_log")
        
    # Verify separation
    assert not hasattr(memory.working_memory, 'audit_history')
    assert not hasattr(memory.short_memory, 'audit_history')

