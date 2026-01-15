import unittest
from commitgen.ai import generate_commit_message

class TestMessageGeneration(unittest.TestCase):

    def test_returns_string(self):
        result = generate_commit_message("some diff")
        self.assertIsInstance(result, str)

    def test_handles_empty_diff(self):
        result = generate_commit_message("")
        self.assertEqual(result, "chore: no changes detected")

    def test_includes_context(self):
        result = generate_commit_message("diff", "my context")
        self.assertIn("my context", result)
