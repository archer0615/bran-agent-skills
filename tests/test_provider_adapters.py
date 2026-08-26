import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
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

    def test_local_http_fixture_exercises_real_transport(self):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append((self.headers.get("Authorization"), json.loads(self.rfile.read(int(self.headers["Content-Length"])))) )
                body = json.dumps({"plan": {"schema_version":"1.0","plan_id":"fixture-plan","goal_id":"g","tasks":[],"dependencies":[],"sequence":[],"risks":[],"human_gates":[]}}).encode()
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            def log_message(self, *_): pass
        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            provider = JsonHttpProvider(f"http://127.0.0.1:{server.server_port}", "fixture-model", "TEST_KEY")
            with patch.dict("os.environ", {"TEST_KEY": "fixture-secret"}):
                result = JsonPlanner(provider).create_plan({"goal_id": "g"})
            self.assertEqual(result["plan_id"], "fixture-plan")
            self.assertEqual(requests[0][0], "Bearer fixture-secret")
            self.assertEqual(requests[0][1]["model"], "fixture-model")
        finally:
            server.shutdown(); thread.join(timeout=2); server.server_close()


if __name__ == "__main__":
    unittest.main()
