# Plan — Layer 3 Runtime Skeleton Implementation

## 1. Setup & Assessment
- [ ] Create `PROJECT.md` at root specifying the architecture and code layout.
- [ ] Set up a heartbeat cron to monitor subagent progress and update `progress.md` periodically.

## 2. Exploration Phase
- [ ] Dispatch `teamwork_preview_explorer` to:
  - Inspect existing files in `agent_runtime/`.
  - Check if the adapter exposes `submit_transition_request()`. If it does not, report that implementation must stop or follow the fallback interface change policy.
  - Formulate implementation strategy for all required modules (`runtime.py`, `planner.py`, `executor.py`, `recovery.py`, `memory.py`, `provider_adapter.py`, `contracts.py`, `interfaces.py`, `exceptions.py`, `runtime_types.py`).

## 3. Implementation Phase (Worker)
- [ ] Dispatch `teamwork_preview_worker` to:
  - Ensure the package structure has EXACTLY the required files (removing/moving extra ones if any, adding missing ones).
  - Implement the skeleton of each module (docstrings, public interfaces, type hints, TODO markers matching `TODO(category): ...`, and test placeholders).
  - Implement `runtime.py` with the loop structure, handling transitions using `request_transition` or `submit_transition_request` (depending on adapter capabilities), proper termination criteria, and exception handling.
  - Implement boundary and recovery tests in the tests directory.

## 4. Verification & Audit Phase
- [ ] Dispatch `teamwork_preview_reviewer` to review code layout, type hints, TODO markers, and logic correctness.
- [ ] Dispatch `teamwork_preview_challenger` to run the test suite and verify boundary and recovery behaviors.
- [ ] Dispatch `teamwork_preview_auditor` to perform forensic integrity verification.

## 5. Synthesis & Final Report
- [ ] Aggregate all results, verify test passes, check audit verdicts.
- [ ] Prepare the final handoff report matching R5.
