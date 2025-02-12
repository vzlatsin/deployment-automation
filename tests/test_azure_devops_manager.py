import unittest
import json
import os
import sys

# Ensure the src directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from azure_manager import AzureDevOpsManager
from deployment_logger import DeploymentLogger  # Ensure this is imported

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")

class TestAzureDevOpsManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load Azure credentials from config file."""
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

        with open(CONFIG_PATH, "r") as config_file:
            config = json.load(config_file)

        cls.azure_pat = config.get("AZURE_DEVOPS_PAT", None)
        if not cls.azure_pat:
            raise ValueError("AZURE_DEVOPS_PAT is missing from config.json")

        cls.organization = "colesgroup"
        cls.project = "ControlM"
        cls.repo_name = "job_count_tracking"
        cls.repo_url = f"https://dev.azure.com/{cls.organization}/{cls.project}/_git/{cls.repo_name}"

        cls.logger = DeploymentLogger()  # Ensure the logger is instantiated

    def test_get_latest_commit(self):
        """Test fetching the latest commit from Azure DevOps."""
        azure_manager = AzureDevOpsManager(
            repo_url=self.repo_url,
            organization=self.organization,
            project=self.project,
            repo_name=self.repo_name,
            access_token=self.azure_pat,
            logger=self.logger
        )
        
        latest_commit = azure_manager.get_latest_commit()
        print(f"Latest Commit: {latest_commit}")  # Debugging

        self.assertIsInstance(latest_commit, str)
        self.assertTrue(len(latest_commit) > 0, "Commit hash should not be empty")

if __name__ == "__main__":
    unittest.main()
