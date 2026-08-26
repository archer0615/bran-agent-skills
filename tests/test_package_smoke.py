import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class PackageSmokeTests(unittest.TestCase):
    def test_module_entrypoint_and_schema_files_are_available(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, "-m", "orchestrator.cli", "doctor", directory], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0)
            self.assertIn('"repository": true', result.stdout)
            self.assertTrue((Path(__file__).parents[1] / "orchestrator" / "schemas" / "provider-config.schema.json").exists())


if __name__ == "__main__":
    unittest.main()
