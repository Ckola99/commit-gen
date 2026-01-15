import unittest
import subprocess
from unittest.mock import patch, MagicMock

from commitgen.git_utils import (
    verify_repo,
    has_staged_changes,
    get_staged_diff,
    stage_all_changes,
)


class TestVerifyRepo(unittest.TestCase):

    @patch("subprocess.run")
    def test_verify_repo_returns_true_when_inside_git_repo(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)

        result = verify_repo()

        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    @patch("subprocess.run")
    def test_verify_repo_returns_false_when_not_in_git_repo(self, mock_run):
        mock_run.return_value = MagicMock(returncode=128)

        result = verify_repo()

        self.assertFalse(result)


class TestHasStagedChanges(unittest.TestCase):

    @patch("subprocess.run")
    def test_has_staged_changes_returns_true_when_changes_are_staged(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)

        result = has_staged_changes()

        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["git", "diff", "--cached", "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    @patch("subprocess.run")
    def test_has_staged_changes_returns_false_when_no_changes_are_staged(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)

        result = has_staged_changes()

        self.assertFalse(result)


class TestGetStagedDiff(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_staged_diff_returns_diff_text_on_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="diff --git a/file.py b/file.py",
        )

        diff = get_staged_diff()

        self.assertEqual(diff, "diff --git a/file.py b/file.py")
        mock_run.assert_called_once_with(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_get_staged_diff_returns_empty_string_on_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)

        diff = get_staged_diff()

        self.assertEqual(diff, "")


class TestStageAllChanges(unittest.TestCase):

    @patch("subprocess.run")
    def test_stage_all_changes_calls_git_add_dot(self, mock_run):
        stage_all_changes()

        mock_run.assert_called_once_with(["git", "add", "."])
