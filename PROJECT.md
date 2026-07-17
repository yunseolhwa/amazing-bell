# Project: Layer 3 Runtime Skeleton for OPS v5

## Architecture
The Layer 3 Runtime is a runtime management skeleton designed to orchestrate agent planning and execution loop logic over existing Layer 0-2 components. It communicates with the kernel and verifier strictly via the `AdapterInterface` and `ProviderAdapter`, ensuring compliance with Kernel Authority constraints.

### Core Modules
- `runtime.py`: Executes the continuous cycle (context sync -> plan -> execute -> transition request -> wait for verifier -> recovery).
- `planner.py`: Forms a plan using the provider adapter; treats context data strictly as data (Prompt Injection Defense).
- `executor.py`: Implements two-phase action records for external side-effects (Action Intent, Action Receipt).
- `recovery.py`: Manages error classification and proposes retry plans without deciding when/how to execute them.
- `memory.py`: Enforces separation between Working Memory and the immutable, read-only Audit History.
- `contracts.py`: Holds domain model behavior rules, constraints, and invariants.
- `interfaces.py`: Defines abstract base interfaces.
- `exceptions.py`: Defines runtime and contract exceptions.
- `runtime_types.py`: Defines typed structures.
- `provider_adapter.py`: Defins interface for LLM provider adapters.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|-------------|--------|
| 1 | Setup & Exploration | Inspect codebase, check adapter capability (`submit_transition_request`), define exact package layout. | None | DONE |
| 2 | Package Structure & Skeleton | Establish exact file list in `agent_runtime/`. Put docstrings, type hints, public APIs, TODOs. | M1 | DONE |
| 3 | Runtime Loop Implementation | Implement main loop logic in `runtime.py` with transition requests instead of state mutations. | M2 | DEFERRED |
| 4 | Boundary & Recovery Tests | Implement specific boundary and recovery test suites. | M3 | DONE |
| 5 | Verification & Review | Review code, run tests via challenger, run forensic auditor checks, synthesize final report. | M4 | DONE |

## Code Layout
- `agent_runtime/`
  - `__init__.py`
  - `runtime.py`
  - `planner.py`
  - `executor.py`
  - `recovery.py`
  - `memory.py`
  - `provider_adapter.py`
  - `contracts.py`
  - `interfaces.py`
  - `exceptions.py`
  - `runtime_types.py`
  - `tests/`
    - `__init__.py`
    - `test_boundary.py`
    - `test_recovery.py`
    - `test_runtime.py`
    - `test_memory.py`

## Interface Contracts
### Runtime Loop ↔ Adapter
- `AdapterInterface.sync_context() -> SystemContext`
- `AdapterInterface.request_transition(state: str, revision: int) -> bool`
- `AdapterInterface.submit_transition_request(transition_request) -> bool` (Check existence)
- `AdapterInterface.wait_for_verifier() -> VerifierResult` (Check existence)
