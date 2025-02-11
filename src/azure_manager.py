# src/azure_manager.py
import sys
import os

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from deployment_logger import DeploymentLogger  # Import the existing logger

class AzureDevOpsManager:
    """
    Handles interactions with Azure DevOps repositories.
    """

    def __init__(self, repo_url, logger: DeploymentLogger):
        self.repo_url = repo_url
        self.logger = logger  # Inject logger
        self.class_name = self.__class__.__name__  # Store class name dynamically

    def push_to_repo(self):
        """
        Simulates pushing code to Azure DevOps.
        """
        self.logger.log_info(f"[{self.class_name}] Pushing to Azure Repo: {self.repo_url}")
        return True

    def compare_with_azure(self, github_commit):
        """
        Compares the latest commit from Azure DevOps with GitHub.
        """
        self.logger.log_info(f"[{self.class_name}] Comparing Azure DevOps repo '{self.repo_url}' with GitHub commit {github_commit}")

        # Stub logic - Replace with API call at work
        azure_commit = "STUB_COMMIT_HASH"

        if github_commit == azure_commit:
            self.logger.log_info(f"[{self.class_name}] Azure DevOps and GitHub are in sync.")
            return True
        else:
            self.logger.log_info(f"[{self.class_name}] Azure DevOps repository is outdated.")
            return False

