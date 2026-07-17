# Context — Layer 3 Runtime Skeleton

## Active Workspace
- Directory: `C:/Users/gram/Documents/antigravity/amazing-bell`

## Package Structure
- Target structure:
  ```text
  agent_runtime/
      __init__.py
      runtime.py
      planner.py
      executor.py
      recovery.py
      memory.py
      provider_adapter.py
      contracts.py
      interfaces.py
      exceptions.py
      runtime_types.py
  ```
- Current files to audit:
  - `agent_runtime/tool_router.py` (needs to be moved/removed to match "exactly" package structure)

## Architectural Constraints
- Prohibited dependencies: `kernel/*`, `verifier/*`, `sqlite3`, `state_storage/*` (Imports must raise `ImportError`/blocked)
- Transition rules: Only `REQUEST` transitions, never set direct states like `COMPLETED`, `FAILED`, or `VERIFYING`.
- Adapter constraint: If `submit_transition_request()` is not exposed, stop immediately and record under Deferred Items.
