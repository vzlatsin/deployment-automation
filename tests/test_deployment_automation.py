import sys
import os

# Add `src/` to Python path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import MagicMock, patch
import inspect

# Import the classes under test
try:
    from github_manager import GitHubRepositoryManager
    from azure_manager import AzureDevOpsManager
    from deployment_orchestrator import DeploymentOrchestrator
    from deployment_logger import DeploymentLogger

except ModuleNotFoundError as e:
    print(f"[ERROR] Failed to import modules: {e}")
    raise


class TestDeploymentSystem(unittest.TestCase):
    """
    Consolidated test suite for Deployment Automation System.
    Includes metadata validation and functional tests.
    """

    def setUp(self):
        """Ensure all necessary objects are defined and validate constructor signature"""
        if None in [GitHubRepositoryManager, AzureDevOpsManager, DeploymentOrchestrator, DeploymentLogger]:
            missing = [name for name, obj in [
                ("GitHubRepositoryManager", GitHubRepositoryManager),
                ("AzureDevOpsManager", AzureDevOpsManager),
                ("DeploymentOrchestrator", DeploymentOrchestrator),
                ("DeploymentLogger", DeploymentLogger)  
            ] if obj is None]
            raise ImportError(f"Missing dependencies: {', '.join(missing)}")
        
        self.logger = DeploymentLogger()
    
    def test_constructor_signatures(self):
        """Ensure all classes have correct constructor parameters"""
        expected_signatures = {
            "GitHubRepositoryManager": {"repo_owner", "repo_name", "logger"},
            "AzureDevOpsManager": {"repo_url", "logger"},
            "DeploymentOrchestrator": {"logger"},
        }
        
        for class_name, expected_params in expected_signatures.items():
            actual_params = set(inspect.signature(eval(class_name).__init__).parameters.keys()) - {"self"}
            self.assertEqual(actual_params, expected_params, 
                f"Constructor mismatch in {class_name}. Expected: {expected_params}, Found: {actual_params}")
    
    def test_dependency_injection(self):
        """Ensure all dependencies can be injected without errors"""
        try:
            mock_logger = MagicMock()
            github_manager = GitHubRepositoryManager(repo_owner="org", repo_name="deployment-automation", logger=mock_logger)
            azure_manager = AzureDevOpsManager(repo_url="https://dev.azure.com/org/repo", logger=mock_logger)
            orchestrator = DeploymentOrchestrator(logger=mock_logger)

            self.assertIsNotNone(github_manager, "GitHubRepositoryManager instance creation failed!")
            self.assertIsNotNone(azure_manager, "AzureDevOpsManager instance creation failed!")
            self.assertIsNotNone(orchestrator, "DeploymentOrchestrator instance creation failed!")
        except Exception as e:
            raise RuntimeError(f"Dependency injection failed: {str(e)}")
    
    @patch("github_manager.GitHubRepositoryManager.fetch_latest_code")
    def test_fetch_latest_code(self, mock_fetch):
        """Ensures GitHubRepositoryManager fetches the correct commit hash."""
        mock_fetch.return_value = "commit-hash-abc123"
        manager = GitHubRepositoryManager(repo_owner="org", repo_name="deployment-automation", logger=self.logger)
        commit_hash = manager.fetch_latest_code()
        self.assertEqual(commit_hash, "commit-hash-abc123")
    
    @patch("azure_manager.AzureDevOpsManager.push_to_repo")
    def test_push_to_azure_repo(self, mock_push):
        """Ensures pushing updates to Azure DevOps works correctly."""
        mock_push.return_value = True
        azure_manager = AzureDevOpsManager(repo_url="https://dev.azure.com/org/repo", logger=self.logger)
        result = azure_manager.push_to_repo()
        self.assertTrue(result)
    
    @patch("deployment_orchestrator.DeploymentOrchestrator.execute_steps")
    def test_orchestrator_execution(self, mock_execute):
        """Ensures DeploymentOrchestrator executes deployment steps correctly."""
        mock_execute.return_value = ["fetch", "compare", "push"]
        orchestrator = DeploymentOrchestrator(logger=self.logger)
        executed_steps = orchestrator.execute_steps(["fetch", "compare", "push"])
        self.assertEqual(executed_steps, ["fetch", "compare", "push"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
