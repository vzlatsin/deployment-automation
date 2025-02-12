import requests
import base64
from deployment_logger import DeploymentLogger

class AzureDevOpsManager:
    """
    Handles interactions with Azure DevOps repositories.
    """

    def __init__(self, repo_url, organization, project, repo_name, access_token, logger: DeploymentLogger):
        self.repo_url = repo_url
        self.organization = organization
        self.project = project
        self.repo_name = repo_name
        self.access_token = access_token
        self.logger = logger  # Inject logger
        self.class_name = self.__class__.__name__  # Store class name dynamically
        self.headers = {"Authorization": f"Basic {self._encode_pat()}", "Content-Type": "application/json"}

    def _encode_pat(self):
        """Encodes the Personal Access Token for Basic Auth."""
        return base64.b64encode(f":{self.access_token}".encode()).decode()

    def push_to_repo(self):
        """
        Simulates pushing code to Azure DevOps.
        """
        self.logger.log_info(f"[{self.class_name}] Pushing to Azure Repo: {self.repo_url}")
        return True  # Keeping the same functionality

    def get_latest_commit(self):
        """
        Fetches the latest commit SHA from Azure DevOps.
        """
        self.logger.log_info(f"[{self.class_name}] Fetching latest commit for repo {self.repo_name}")

        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/git/repositories/{self.repo_name}/commits?api-version=6.0"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises an error for non-200 responses
            commits = response.json().get("value", [])
            if commits:
                latest_commit_sha = commits[0]["commitId"]
                self.logger.log_info(f"[{self.class_name}] Latest Azure DevOps commit: {latest_commit_sha}")
                return latest_commit_sha
            else:
                self.logger.log_warning(f"[{self.class_name}] No commits found in Azure DevOps repository.")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"[{self.class_name}] Azure API request failed: {e}")
            return None

    def compare_with_azure(self, github_commit):
        """
        Compares the latest commit from Azure DevOps with GitHub.
        """
        self.logger.log_info(f"[{self.class_name}] Comparing Azure DevOps repo '{self.repo_url}' with GitHub commit {github_commit}")

        azure_commit = self.get_latest_commit()

        if azure_commit is None:
            self.logger.log_error(f"[{self.class_name}] Failed to retrieve latest commit from Azure DevOps.")
            return False

        if github_commit == azure_commit:
            self.logger.log_info(f"[{self.class_name}] Azure DevOps and GitHub are in sync.")
            return True
        else:
            self.logger.log_info(f"[{self.class_name}] Azure DevOps repository is outdated.")
            return False
