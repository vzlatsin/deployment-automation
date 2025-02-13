import unittest
import sys
from unittest.mock import patch, MagicMock

# ✅ Fix ImportError: Add src directory to system path
sys.path.insert(0, "src")  # Adjust based on your project structure

from azure_manager import AzureDevOpsManager
from deployment_logger import DeploymentLogger

class TestAzureAPIFailure(unittest.TestCase):
    """Test Azure API failure separately."""

    def setUp(self):
        """Set up test with mock logger."""
        self.mock_logger = MagicMock(spec=DeploymentLogger)
        self.manager = AzureDevOpsManager(
            repo_url="https://dev.azure.com/test-org/test-repo",
            organization="test-org",
            project="test-project",
            repo_name="test-repo",
            access_token="fake-token",
            logger=self.mock_logger
        )

    @patch("azure_manager.requests.get")
    def test_compare_with_azure_api_failure(self, mock_get):
        """Test case where Azure DevOps API returns an error."""
        # Mock API response with failure
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"

        result = self.manager.compare_with_azure("123456")

        # Ensure function correctly returns False on failure
        self.assertFalse(result)  

        # 🐛 Debugging step: Print captured logs
        print("Captured Logs:", self.mock_logger.method_calls)

        # ✅ Verify log messages
        logged_errors = [call[0][0] for call in self.mock_logger.log_error.call_args_list]
        
        self.assertIn(
            "[AzureDevOpsManager] Azure API request failed: 500 - Internal Server Error",
            logged_errors
        )

if __name__ == "__main__":
    unittest.main()
