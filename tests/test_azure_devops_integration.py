import unittest
import json
import requests
import base64
import logging
import sys
import os

# Ensure the `src/` folder is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

print("Updated PYTHONPATH:", sys.path)  # Debugging step

from azure_manager import AzureDevOpsManager  # Ensure this is correctly imported

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

from unittest.mock import MagicMock, patch

class TestAzureDevOpsIntegration(unittest.TestCase):
    """ Integration tests for Azure DevOps API (No Mocks) """

    @classmethod
    def setUpClass(cls):
        """ Load config and prepare authentication """
        try:
            config_path = os.path.join(os.path.dirname(__file__), "resources/config.json")
            with open(config_path, "r") as file:
                cls.config = json.load(file)
            logging.debug("Loaded config.json successfully.")

            # Validate required fields
            required_keys = ["AZURE_ORGANIZATION", "AZURE_PROJECT", "AZURE_REPO", "AZURE_DEVOPS_PAT", "AZURE_BASE_URL"]
            for key in required_keys:
                if key not in cls.config:
                    raise KeyError(f"Missing required key in config.json: {key}")

            cls.organization = cls.config["AZURE_ORGANIZATION"]
            cls.project = cls.config["AZURE_PROJECT"]
            cls.repo_name = cls.config["AZURE_REPO"]
            cls.pat = cls.config["AZURE_DEVOPS_PAT"]
            cls.base_url = cls.config["AZURE_BASE_URL"]

            cls.repo_url = f"{cls.base_url}/{cls.organization}/{cls.project}/_git/{cls.repo_name}"

            cls.auth_header = {
                "Authorization": f"Basic {base64.b64encode(f':{cls.pat}'.encode()).decode()}"
            }

            mock_logger = MagicMock()
            mock_logger.log_info = MagicMock()  # ✅ Ensure log_info is mocked
            mock_logger.log_error = MagicMock()
            

            # Initialize AzureDevOpsManager with repo_url
            cls.azure_manager = AzureDevOpsManager(
                organization=cls.organization,
                project=cls.project,
                repo_name=cls.repo_name,
                repo_url=cls.repo_url,
                access_token=cls.pat,
                logger=mock_logger 
            )

        except Exception as e:
            logging.error(f"Failed to load config.json or initialize AzureDevOpsManager: {e}")
            raise

    def test_authenticate_with_azure(self):
        """ Test: Authenticate with Azure DevOps and get repository list """
        url = f"https://dev.azure.com/{self.organization}/_apis/git/repositories?api-version=6.0"
        logging.debug("Azure API URL: %s", url)

        response = requests.get(url, headers=self.auth_header)
        logging.debug("Received response: %s %s", response.status_code, response.reason)

        self.assertEqual(response.status_code, 200, "Authentication failed!")
        self.assertIn("value", response.json(), "Response does not contain 'value' key")
        logging.info("✅ Authentication successful! Repository count: %d", len(response.json()["value"]))

    def test_get_latest_commit(self):
        """ Test fetching the latest commit from Azure DevOps """
        repo_name = self.config.get("AZURE_REPO")
        project = self.config.get("AZURE_PROJECT")

        if not repo_name or not project:
            self.fail("AZURE_REPO or AZURE_PROJECT is missing in config.json")

        logging.info(f"Fetching latest commit for repo: {repo_name}")
        latest_commit = self.azure_manager.get_latest_commit()  # ✅ No arguments needed


        self.assertIsNotNone(latest_commit, "Latest commit should not be None")
        self.assertIsInstance(latest_commit, str, "Commit hash should be a string")
        self.assertTrue(len(latest_commit) > 5, "Commit hash should be a valid length")
        logging.info(f"✅ Latest commit fetched successfully: {latest_commit}")

if __name__ == "__main__":
    unittest.main()
