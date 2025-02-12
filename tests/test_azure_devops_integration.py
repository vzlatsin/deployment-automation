import unittest
import json
import requests
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class TestAzureDevOpsIntegration(unittest.TestCase):
    """ Integration tests for Azure DevOps API (No Mocks) """

    @classmethod
    def setUpClass(cls):
        """ Load config and prepare authentication """
        try:
            with open("config/config.json", "r") as f:
                cls.config = json.load(f)
            logging.debug("Loaded config.json successfully.")
        except Exception as e:
            logging.error("Failed to load config.json: %s", e)
            raise

        cls.pat = cls.config.get("AZURE_DEVOPS_PAT")
        cls.organization = cls.config.get("AZURE_DEVOPS_ORG", "colesgroup")  # Default org name

        if not cls.pat:
            raise ValueError("AZURE_DEVOPS_PAT is missing in config.json")

        cls.auth_header = {
            "Authorization": f"Basic {base64.b64encode(f':{cls.pat}'.encode()).decode()}"
        }

    def test_authenticate_with_azure(self):
        """ Test: Authenticate with Azure DevOps and get repository list """
        url = f"https://dev.azure.com/{self.organization}/_apis/git/repositories?api-version=6.0"
        logging.debug("Azure API URL: %s", url)

        response = requests.get(url, headers=self.auth_header)
        logging.debug("Received response: %s %s", response.status_code, response.reason)

        self.assertEqual(response.status_code, 200, "Authentication failed!")
        self.assertIn("value", response.json(), "Response does not contain 'value' key")
        logging.info("✅ Authentication successful! Repository count: %d", len(response.json()["value"]))

if __name__ == "__main__":
    unittest.main()
