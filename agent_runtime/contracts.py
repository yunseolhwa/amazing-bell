"""
Behavioral rules, runtime contracts, and invariants for the Layer 3 Agent Runtime.

This module contains validators to enforce that the runtime conforms to state machine
rules and does not generate forbidden states or invalid transitions.
"""

from .exceptions import RuntimeContractViolation

__all__ = ["RuntimeContractValidator"]

# TODO(contract): Expand contract checks to validate allowed transitions based on SystemContext.
# TODO(test): Verify contract validator in test_boundary.py.


class RuntimeContractValidator:
    """Enforces behavioral rules and invariants for the Layer 3 Agent Runtime."""

    FORBIDDEN_STATES = {"COMPLETED"}  # COMPLETED is strictly a kernel-managed terminal state.

    @classmethod
    def validate_state(cls, state: str) -> None:
        """
        Validates that the target state is allowed to be generated/requested by the runtime.
        Raises RuntimeContractViolation if the state is forbidden.
        """
        if state in cls.FORBIDDEN_STATES:
            raise RuntimeContractViolation(
                f"State '{state}' is forbidden. The runtime is not permitted to request transitions to this state."
            )

    @classmethod
    def validate_transition(cls, current_state: str, target_state: str) -> None:
        """
        Validates the transition from current_state to target_state.
        Ensures that invariants are maintained.
        """
        cls.validate_state(target_state)
        # Additional invariant: Runtime should not transition from WAITING back to WAITING, etc.
        if current_state == "WAITING" and target_state == "WAITING":
            raise RuntimeContractViolation("Redundant transition: already in WAITING state.")

