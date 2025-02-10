# src/deployment_orchestrator.py
import sys
import os

# Add `src/` to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from deployment_logger import DeploymentLogger
from github_manager import GitHubRepositoryManager  # Import GitHub manager

class DeploymentOrchestrator:
    """
    Manages execution of deployment steps.
    """

    def __init__(self, logger: DeploymentLogger, github_manager: GitHubRepositoryManager):
        self.logger = logger  # Inject logger
        self.github_manager = github_manager  # Inject GitHub manager
        self.class_name = self.__class__.__name__  # Store class name dynamically

    def execute_steps(self, steps):
        """
        Executes the requested deployment steps.
        """
        self.logger.log_info(f"[{self.class_name}] Executing deployment steps: {steps}")

        for step in steps:
            if step == "fetch":
                try:
                    latest_commit = self.github_manager.fetch_latest_commit()
                    self.logger.log_info(f"[{self.class_name}] Fetched latest commit: {latest_commit}")
                except Exception as e:
                    self.logger.log_error(f"[{self.class_name}] Failed to fetch latest commit: {str(e)}")

        self.logger.log_info(f"Steps executed: {steps}")
        return steps
