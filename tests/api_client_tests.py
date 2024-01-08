"""Testing for API client objects"""
import unittest
from unittest.mock import patch

from api_client import load_environment_secrets


class TestLoadEnvironmentSecrets(unittest.TestCase):
    """Testing for `load_environment_secrets` function"""

    @patch("os.getenv")
    def test_default_dotenv_path(self, mock_getenv):
        """Test load from default .env path"""
        mock_getenv.side_effect = ["user123", "pass123"]
        self.assertEqual(load_environment_secrets(), ("user123", "pass123"))

    @patch("os.getenv")
    def test_missing_credentials(self, mock_getenv):
        """Assert that missing credentials raise an error"""
        mock_getenv.side_effect = [None, None]
        with self.assertRaises(RuntimeError):
            load_environment_secrets()


if __name__ == "__main__":
    unittest.main()
