import sys
import os

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from deployment_logger import DeploymentLogger  # Import the new logger


class GitHubRepositoryManager:
    """
    Manages interactions with a GitHub repository.
    """

    def __init__(self, repo_owner, repo_name, logger: DeploymentLogger):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.logger = logger  # Inject logger
        self.class_name = self.__class__.__name__  # Store class name dynamically

    def fetch_latest_code(self):
        """
        Simulates fetching the latest commit hash from GitHub.
        """
        self.logger.log_info(f"[{self.class_name}] Fetching latest commit for {self.repo_owner}/{self.repo_name}")
        return "stub-commit-hash"
