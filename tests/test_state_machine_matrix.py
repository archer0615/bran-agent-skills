import unittest

from orchestrator.state_machine import StateMachine, TERMINAL_STATES


class StateMachineMatrixTests(unittest.TestCase):
    def test_every_declared_transition_accepts_required_context(self):
        machine = StateMachine()
        values = {"goal_id": "g", "plan_id": "p", "task_id": "t", "reason": "test", "execution_result": {}, "verification": {}, "retry": 1, "review": {}, "plan_revision": 1, "recovery": {}, "approval": {"status": "APPROVED"}}
        for rule in machine.transitions:
            context = {key: values.get(key, "present") for key in rule.required_context}
            machine.transition(rule.from_state, rule.to_state, rule.owner, context)

    def test_terminal_states_are_fail_closed(self):
        machine = StateMachine()
        for state in TERMINAL_STATES:
            with self.assertRaises(Exception):
                machine.transition(state, "PLANNING", "Controller", {"goal_id": "g"})


if __name__ == "__main__":
    unittest.main()
