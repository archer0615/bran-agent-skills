import contextlib
import io
import json
import tempfile
import unittest

from orchestrator.cli import main


class GateCliTests(unittest.TestCase):
    def test_request_gate_then_list_and_reject(self):
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["request-gate", directory, "--gate-id", "task-1", "--reason", "review migration"]), 0)
            gate = json.loads(output.getvalue())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["gates", directory]), 0)
                self.assertEqual(main(["reject", directory, "--gate-id", gate["gate_id"], "--reason", "not approved"]), 0)


if __name__ == "__main__":
    unittest.main()
