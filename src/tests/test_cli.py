import unittest
from unittest.mock import patch
from typer.testing import CliRunner
import typer

from commitgen.cli import app

runner = CliRunner()


class TestCLI(unittest.TestCase):

    # ---------- Early exits ----------

    @patch("commitgen.cli.git_utils.verify_repo", return_value=False)
    def test_commit_not_git_repo(self, _):
        result = runner.invoke(app, ["commit"])
        self.assertNotEqual(result.exit_code, 0)

    @patch("commitgen.cli.git_utils.verify_repo", return_value=True)
    @patch("commitgen.cli.git_utils.has_staged_changes", return_value=False)
    @patch("commitgen.cli.typer.confirm", return_value=False)
    def test_commit_no_staged_changes_abort(self, *_):
        result = runner.invoke(app, ["commit"])
        self.assertNotEqual(result.exit_code, 0)

    # ---------- Happy path: accept ----------

    @patch("commitgen.cli.git_utils.commit_changes")
    @patch("commitgen.cli.ai.generate_commit_message", return_value="[FEAT]: add login")
    @patch("commitgen.cli.git_utils.get_staged_diff", return_value="diff --git a b")
    @patch("commitgen.cli.git_utils.has_staged_changes", return_value=True)
    @patch("commitgen.cli.git_utils.verify_repo", return_value=True)
    @patch("commitgen.cli.typer.prompt", return_value="a")
    def test_commit_accept_flow(
        self,
        _prompt,
        _verify,
        _staged,
        _diff,
        _ai,
        commit_mock,
    ):
        result = runner.invoke(app, ["commit"])
        self.assertEqual(result.exit_code, 0)
        commit_mock.assert_called_once()

    # ---------- Regenerate path ----------

    @patch("commitgen.cli.git_utils.commit_changes")
    @patch("commitgen.cli.ai.generate_commit_message", side_effect=[
        "[FEAT]: add login",
        "[FIX]: fix bug"
    ])
    @patch("commitgen.cli.git_utils.get_staged_diff", return_value="diff")
    @patch("commitgen.cli.git_utils.has_staged_changes", return_value=True)
    @patch("commitgen.cli.git_utils.verify_repo", return_value=True)
    @patch("commitgen.cli.typer.prompt", side_effect=["r", "extra context", "a"])
    def test_commit_regenerate_flow(
        self,
        _prompt,
        _verify,
        _staged,
        _diff,
        _ai,
        commit_mock,
    ):
        result = runner.invoke(app, ["commit"])
        self.assertEqual(result.exit_code, 0)
        commit_mock.assert_called_once()

    # ---------- Quit path ----------

    @patch("commitgen.cli.git_utils.get_staged_diff", return_value="diff")
    @patch("commitgen.cli.git_utils.has_staged_changes", return_value=True)
    @patch("commitgen.cli.git_utils.verify_repo", return_value=True)
    @patch("commitgen.cli.typer.prompt", return_value="q")
    def test_commit_quit(
        self,
        _prompt,
        _verify,
        _staged,
        _diff,
    ):
        result = runner.invoke(app, ["commit"])
        self.assertNotEqual(result.exit_code, 0)

    # ---------- Version command ----------

    def test_version_command(self):
        result = runner.invoke(app, ["version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("CommitGen version", result.output)

    # ---------- Config command ----------

    @patch("commitgen.cli.CONFIG_FILE")
    @patch("commitgen.cli.CONFIG_DIR")
    @patch("commitgen.cli.typer.prompt", return_value="fake-key")
    def test_config_command(self, *_):
        result = runner.invoke(app, ["config"])
        self.assertEqual(result.exit_code, 0)
