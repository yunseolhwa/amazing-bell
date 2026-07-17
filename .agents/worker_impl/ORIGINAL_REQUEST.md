## 2026-07-17T01:19:00Z
You are the teamwork_preview_worker subagent.
Your identity is worker_impl.
Your working directory is C:/Users/gram/Documents/antigravity/amazing-bell/.agents/worker_impl.
Your parent is orchestrator (conversation ID: ce913f74-81ab-4461-957f-ba8ae3523ad0).

Your mission is to perform Phase 1 (Package Creation) and Phase 2 (Skeleton Implementation) for the Layer 3 Runtime in C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime.

Detailed instructions:
1. Ensure the `agent_runtime/` package has EXACTLY the required files (removing `tool_router.py` or moving it out, and creating `interfaces.py`, `exceptions.py`, `runtime_types.py`, and `provider_adapter.py`).
2. Move class definitions and interfaces from `contracts.py` to their correct files:
   - Move `AdapterInterface` and `ProviderAdapter` ABCs to `interfaces.py`.
   - Move `SystemContext`, `Artifact`, `ExecutionResult`, `Plan`, and `ErrorClassification` to `runtime_types.py`.
   - Move `RevisionMismatchError` to `exceptions.py`.
   - Keep only behavioral rules, runtime contracts, and invariants in `contracts.py`. E.g., add a function/class to validate that the runtime doesn't generate forbidden states (COMPLETED, FAILED, VERIFYING).
3. Update imports in all existing files: `runtime.py`, `planner.py`, `executor.py`, `recovery.py`, `memory.py`, `__init__.py`, and all test files in `tests/` so they import from the correct reorganized files.
4. Ensure every module contains:
   - Module docstring
   - Public interfaces/exports
   - Type hints
   - TODO markers in exactly this format: `# TODO(category): detailed description` (categories like `runtime`, `test`, `contract`, `provider`, `memory`)
   - Unit test placeholder (already exists or add if missing)
5. In `runtime.py`, implement the skeleton of the main loop. BUT wait:
   - Check if the adapter exposes `submit_transition_request()` and `wait_for_verifier()`.
   - Since it doesn't, do not invent the API on the adapter.
   - Per the Interface Change Policy and user requirements, stop implementation immediately where those APIs are needed, or write a check that stops runtime execution or raises an error, and document this as a deferred dependency.
6. Verify your implementation by running the test suite via pytest. Make sure all existing and any new test placeholders pass.
7. Write a detailed handoff report in C:/Users/gram/Documents/antigravity/amazing-bell/.agents/worker_impl/handoff.md detailing what you modified, which files were created/deleted, the test run outputs, and list the missing adapter APIs as deferred items.
8. Send a message to the orchestrator (conversation ID: ce913f74-81ab-4461-957f-ba8ae3523ad0) once you are done.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
