## 2026-07-17T01:21:31Z

You are the teamwork_preview_worker subagent.
Your identity is worker_tests.
Your working directory is C:/Users/gram/Documents/antigravity/amazing-bell/.agents/worker_tests.
Your parent is orchestrator (conversation ID: ce913f74-81ab-4461-957f-ba8ae3523ad0).

Your mission is to implement:
1. Custom exceptions in C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime/exceptions.py:
   - `RevisionMismatchError`
   - `RuntimeContractViolation`
   - `AccessError`
   - `RecoveryError`
2. Update C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime/contracts.py to use `RuntimeContractViolation` instead of `ValueError` when state transition rules are violated.
3. Update C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime/__init__.py or C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime/runtime.py to enforce prohibited import boundaries.
   Add a sys.meta_path hook `ForbiddenModuleBlocker` that intercepts imports:
   - If importing `sqlite3` or any module starting with `verifier` or `state_storage`, raise `AccessError`.
   - If importing any module starting with `kernel`, raise `ImportError`.
4. Implement the following specific boundary tests in C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime/tests/test_boundary.py:
   - `Test_Runtime_CannotImportKernel` (Expected: Import blocked / ImportError)
     Attempt to import a mock `kernel` module or trigger the meta_path hook to raise `ImportError`.
   - `Test_Runtime_CannotUseSQLite` (Expected: forbidden / AccessError)
     Attempt to import `sqlite3` and expect `AccessError`.
   - `Test_Runtime_CannotSetCompleted` (Expected: RuntimeContractViolation)
     Verify that trying to transition to `COMPLETED` raises `RuntimeContractViolation`.
   - `Test_Runtime_CannotCallVerifier` (Expected: forbidden / AccessError)
     Attempt to import `verifier` and expect `AccessError`.
   - `Test_Runtime_CannotBypassAdapter` (Expected: RuntimeContractViolation)
     Verify that the runtime cannot perform state transitions or updates outside of the adapter, raising `RuntimeContractViolation`.
5. Implement the following specific recovery tests in C:/Users/gram/Documents/antigravity/amazing-bell/agent_runtime/tests/test_recovery.py:
   - `Crash Recovery`: Given pending receipt, Expect context restored (already exists as `test_crash_recovery_with_receipt`, ensure it matches).
   - `Retry Budget`: Given retry_count == limit, Expect retry proposal rejected (already exists as `test_retry_budget_exhaustion`, ensure it matches).
   - `Unknown Receipt`: Expect request manual verification (assert that if a receipt is unknown, `RecoveryManager` returns `"WAITING"` or raises `RecoveryError` to request manual verification).
   - `Revision Mismatch`: Expect abort execution (assert that if a `RevisionMismatchError` is raised in the runtime loop and cannot be resolved, execution aborts or propagates).
6. Verify your implementation by running pytest on the host machine. Ensure all 10+ tests pass.
7. Write a detailed handoff report in C:/Users/gram/Documents/antigravity/amazing-bell/.agents/worker_tests/handoff.md detailing what you modified, the test run outputs, and verification details.
8. Send a message to the orchestrator (conversation ID: ce913f74-81ab-4461-957f-ba8ae3523ad0) once you are done.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
