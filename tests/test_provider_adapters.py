import json
import unittest
from unittest.mock import patch

from orchestrator.provider_adapters import JsonHttpProvider, JsonPlanner, JsonReviewer


class _Response:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return json.dumps(self.payload).encode()


class ProviderAdapterTests(unittest.TestCase):
    def test_planner_and_reviewer_parse_structured_contracts(self):
        planner_response = {"plan": {"schema_version":"1.0","plan_id":"p","goal_id":"g","tasks":[],"dependencies":[],"sequence":[],"risks":[],"human_gates":[]}}
        reviewer_response = {"review": {"schema_version":"1.0","task_id":"t","decision":"PASS","acceptance_results":[],"issues":[],"required_corrections":[],"risk_findings":[],"next_action":"finish"}}
        provider = JsonHttpProvider("https://provider.invalid", "model", "TEST_KEY")
        with patch.dict("os.environ", {"TEST_KEY": "present"}):
            with patch("urllib.request.urlopen") as urlopen:
                response = _Response(); response.payload = planner_response; urlopen.return_value = response
                self.assertEqual(JsonPlanner(provider).create_plan({"goal_id":"g"})["plan_id"], "p")
                response.payload = reviewer_response
                self.assertEqual(JsonReviewer(provider).review({"task_id":"t"}, {})["decision"], "PASS")


if __name__ == "__main__":
    unittest.main()
