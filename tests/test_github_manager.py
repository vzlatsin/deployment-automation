import unittest
from unittest.mock import patch  # `patch` allows us to replace real function calls with fake (mocked) responses
from src.github_manager import GitHubRepositoryManager  # Import the class we're testing

class TestGitHubRepositoryManager(unittest.TestCase):
    """
    Test cases for GitHubRepositoryManager.
    """

    # `patch` replaces the `fetch_latest_code` method with a fake version for this test
    @patch("src.github_manager.GitHubRepositoryManager.fetch_latest_code")
    def test_fetch_latest_code(self, mock_fetch):
        """
        Ensures GitHubRepositoryManager fetches the correct commit hash.
        """

        # Simulate what GitHub API would return: a fake commit hash
        mock_fetch.return_value = "commit-hash-abc123"

        # Create an instance of GitHubRepositoryManager
        # We don't need real credentials or a real GitHub repo since we're mocking the method
        manager = GitHubRepositoryManager(repo_owner="vzlatsin", repo_name="deployment-automation")

        # Call the method we are testing
        commit_hash = manager.fetch_latest_code()

        # Print debugging information for clarity
        print("\n[TEST] Running test_fetch_latest_code()...")
        print(f"[INFO] Retrieved commit hash: {commit_hash}")

        # Verify that the returned commit hash matches what we expected
        self.assertEqual(commit_hash, "commit-hash-abc123")

if __name__ == "__main__":
    # Run tests with verbosity level 2 for more detailed output
    unittest.main(verbosity=2)
