import unittest

from orchestrator.contracts import ContractValidationError, validate_artifact


class ContractTests(unittest.TestCase):
    def test_valid_goal_is_accepted(self) -> None:
        goal = {
            "schema_version": "1.0",
            "goal_id": "goal-1",
            "objective": "Create a feature",
            "repository": {"path": ".", "revision": "abc"},
            "constraints": [],
            "acceptance_criteria": [],
            "risk_level": "low",
        }
        self.assertEqual(validate_artifact("goal", goal), goal)

    def test_missing_and_unknown_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(ContractValidationError, "missing required fields"):
            validate_artifact("task", {"schema_version": "1.0"})

        task = {
            "schema_version": "1.0",
            "task_id": "task-1",
            "plan_id": "plan-1",
            "objective": "Implement",
            "scope": [],
            "allowed_changes": [],
            "forbidden_changes": [],
            "acceptance_criteria": [],
            "required_verification": [],
            "dependencies": [],
            "risk_level": "low",
            "unexpected": True,
        }
        with self.assertRaisesRegex(ContractValidationError, "unknown fields"):
            validate_artifact("task", task)

    def test_enum_and_schema_version_are_rejected(self) -> None:
        with self.assertRaises(ContractValidationError):
            validate_artifact("review_result", {
                "schema_version": "1.0", "task_id": "task-1", "decision": "MAYBE",
                "acceptance_results": [], "issues": [], "required_corrections": [],
                "risk_findings": [], "next_action": "finish",
            })

        with self.assertRaises(ContractValidationError):
            validate_artifact("goal", {
                "schema_version": "2.0", "goal_id": "goal-1", "objective": "x",
                "repository": {}, "constraints": [], "acceptance_criteria": [], "risk_level": "low",
            })


if __name__ == "__main__":
    unittest.main()
