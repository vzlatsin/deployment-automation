import sys
import os

# Ensure `src/` is in the module path so we can import `github_manager.py`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import patch  # Import `patch` to mock API calls
import requests
from github_manager import GitHubRepositoryManager
from deployment_logger import DeploymentLogger  # Import logger

class TestGitHubRepositoryManager(unittest.TestCase):
    """
    Test suite for GitHubRepositoryManager.
    Ensures API interactions are correctly handled, including error cases.
    """

    def setUp(self):
        """Initialize logger and repository manager."""
        self.mock_logger = DeploymentLogger()
        self.manager = GitHubRepositoryManager("test_owner", "test_repo", self.mock_logger)

    @patch("github_manager.requests.get")  # Mock `requests.get` so no real API call is made
    def test_fetch_latest_commit_success(self, mock_get):
        """Test successful retrieval of latest commit hash."""
        # Simulate API response with a 200 status and a commit hash
        mock_get.return_value.status_code = 200  # Fake a successful response
        mock_get.return_value.json.return_value = [{"sha": "abc123"}]  # Fake commit data

        # Run the function (it will use mock_get instead of real requests.get)
        commit_hash = self.manager.fetch_latest_commit()

        # Check if the function returned the correct commit hash
        self.assertEqual(commit_hash, "abc123")  # Expected output: "abc123"

    @patch("github_manager.requests.get")  # Mock API request to simulate failure
    def test_fetch_latest_commit_api_failure(self, mock_get):
        """Test handling of GitHub API errors (e.g., server errors)."""
        # Simulate a 500 Internal Server Error response from GitHub
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"

        # Expect `fetch_latest_commit()` to raise an exception
        with self.assertRaises(Exception) as context:
            self.manager.fetch_latest_commit()

        # Verify the error message contains "GitHub API error"
        self.assertIn("GitHub API error", str(context.exception))

    @patch("github_manager.requests.get")  # Mock network failure scenario
    def test_fetch_latest_commit_network_failure(self, mock_get):
        """Test handling of network failures (timeouts, connection issues)."""
        # Simulate a network error (e.g., timeout or no internet connection)
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Expect `fetch_latest_commit()` to raise an exception
        with self.assertRaises(Exception) as context:
            self.manager.fetch_latest_commit()

        # Verify the raised exception contains "Network error"
        self.assertIn("Network error", str(context.exception))

if __name__ == "__main__":
    unittest.main(verbosity=2)  # Run tests with detailed output
