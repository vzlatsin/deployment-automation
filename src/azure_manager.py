# src/azure_manager.py
import sys
import os

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from deployment_logger import DeploymentLogger  # Import the new logger

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
