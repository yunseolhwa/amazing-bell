# OPS v5 Layer 3 Agent Runtime

This repository contains the **Layer 3 Runtime Skeleton** implementation for the OPS v5 architecture. It is built strictly on top of Layer 0 (Kernel), Layer 1 (Adapter), and Layer 2 (Verifier), maintaining strict architectural boundaries and state authority isolation.

## Project Structure

```text
agent_runtime/
├── __init__.py           # Package entrypoint
├── runtime.py            # Main agent runtime loop (sync, plan, execute, verify, recover)
├── planner.py            # Core planner skeleton
├── executor.py           # Core executor skeleton implementing two-phase action records
├── recovery.py           # Crash recovery and retry budget logic
├── memory.py             # Working memory and read-only audit logs
├── provider_adapter.py   # LLM provider abstraction layer
├── contracts.py          # Behavioral rules, invariants, and context contracts
├── interfaces.py         # Abstract interfaces, Protocol and ABC definitions
├── exceptions.py         # Custom runtime exceptions
├── runtime_types.py      # Common types and models
└── tests/                # Test suite
    ├── __init__.py
    ├── test_boundary.py  # Architectural boundary validation tests
    ├── test_memory.py    # Memory isolation tests
    ├── test_recovery.py  # Crash recovery policy tests
    └── test_runtime.py   # Runtime main loop tests
```

---

## Architecture Boundaries

- **State Isolation**: The runtime cannot mutably write to the SQLite database or directly invoke internal Kernel transition operations.
- **Dependency Restrictions**: Import hooks are validated in test environments to ensure `agent_runtime` never imports `kernel`, `verifier`, or `sqlite3`.
- **Two-Phase Commit**: Tool execution requiring mutations follows the Intent-Receipt protocol to prevent duplicate actions on crash.

---

## Test Execution & Verification

### Local Prerequisites
Ensure you have Python 3.10+ and `pytest` installed.
```bash
pip install pytest
```

### Running Tests
To execute the test suite and verify the architectural boundary/recovery constraints:
```bash
pytest agent_runtime/tests
```

### Last Verification Result
```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\gram\Documents\antigravity\amazing-bell
collected 15 items

agent_runtime\tests\test_boundary.py ......                              [ 40%]
agent_runtime\tests\test_memory.py .                                     [ 46%]
agent_runtime\tests\test_recovery.py ......                              [ 86%]
agent_runtime\tests\test_runtime.py ..                                   [100%]

============================= 15 passed in 0.06s ==============================
```
