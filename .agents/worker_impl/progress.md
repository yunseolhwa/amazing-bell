# Progress Tracker - Layer 3 Agent Runtime Reorganization

Last visited: 2026-07-17T10:19:00+09:00

## Milestone 1: Phase 1 (Package Creation)
- [x] Extract custom types, exceptions, and interfaces from `contracts.py`
- [x] Create `interfaces.py`, `exceptions.py`, `runtime_types.py`, and `provider_adapter.py`
- [x] Move `tool_router.py` out of `agent_runtime/` package
- [x] Clean `contracts.py` to only contain rules and invariants (added `RuntimeContractValidator`)

## Milestone 2: Phase 2 (Skeleton Implementation)
- [x] Update imports in all existing files (`runtime.py`, `planner.py`, `executor.py`, `recovery.py`, `memory.py`, `__init__.py`)
- [x] Update imports in all test files (`tests/test_runtime.py`, `tests/test_boundary.py`, `tests/test_memory.py`, `tests/test_recovery.py`)
- [x] Implement check in `runtime.py` main loop for missing `submit_transition_request` and `wait_for_verifier` APIs, raising `NotImplementedError` per Interface Change Policy
- [x] Update tests mock adapters to mock new APIs to retain backward compatibility with legacy tests
- [x] Add new unit test `test_missing_apis_raises_not_implemented` to verify correct error raising
- [x] Ensure every module has docstring, `__all__`, type hints, TODO markers, and unit test placeholders
- [x] Run test suite and verify 8/8 tests pass successfully
