import unittest
import os
from unittest.mock import patch
import typer
from commitgen.config import ensure_api_key


class TestConfig(unittest.TestCase):

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("commitgen.config.load_config")
    def test_ensure_api_key_success(self, _):
        key = ensure_api_key()
        self.assertEqual(key, "test-key")

    @patch.dict(os.environ, {}, clear=True)
    @patch("commitgen.config.load_config")
    def test_ensure_api_key_missing(self, _):
        with self.assertRaises(typer.Exit):
            ensure_api_key()
