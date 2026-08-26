import tempfile
import unittest
from pathlib import Path

from orchestrator.session import ResumeError, Session


class SessionTests(unittest.TestCase):
    def test_resume_requires_same_repository_and_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            session = Session.start(directory, "abc")
            session.validate_resume(Path(directory), "abc")
            with self.assertRaises(ResumeError):
                session.validate_resume(directory, "def")


if __name__ == "__main__":
    unittest.main()
