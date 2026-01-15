import unittest
from unittest.mock import patch, MagicMock
import subprocess
from commitgen.git_utils import verify_repo

class TestVerifyRepo(unittest.TestCase):

    @patch('subprocess.run')
    def test_verify_repo_true(self, mock_run):
        # Setup: Simulate git returning 0 (success/inside a repo)
        mock_run.return_value = MagicMock(returncode=0)

        self.assertTrue(verify_repo())
        # Verify the command was called with the correct arguments
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    @patch('subprocess.run')
    def test_verify_repo_false(self, mock_run):
        # Setup: Simulate git returning 128 (fatal: not a git repository)
        mock_run.return_value = MagicMock(returncode=128)

        self.assertFalse(verify_repo())
