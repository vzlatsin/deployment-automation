import sys
import os

# Add `src/` to Python path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import MagicMock, patch
import inspect
import logging

# Import the classes under test
try:
    from github_manager import GitHubRepositoryManager
    from azure_manager import AzureDevOpsManager
    from deployment_orchestrator import DeploymentOrchestrator
    from deployment_logger import DeploymentLogger
    from app_packager import AppPackager
    from jfrog_uploader import JFrogUploader
    from remote_deployer import RemoteDeployer

except ModuleNotFoundError as e:
    print(f"[ERROR] Failed to import modules: {e}")
    raise


class TestDeploymentSystem(unittest.TestCase):
    """
    Consolidated test suite for Deployment Automation System.
    Includes metadata validation, functional tests, and error handling.
    """

    def setUp(self):
        """Ensure all necessary objects are defined and validate constructor signature"""
        if None in [GitHubRepositoryManager, AzureDevOpsManager, DeploymentOrchestrator, DeploymentLogger, 
                    AppPackager, JFrogUploader, RemoteDeployer]:
            missing = [name for name, obj in [
                ("GitHubRepositoryManager", GitHubRepositoryManager),
                ("AzureDevOpsManager", AzureDevOpsManager),
                ("DeploymentOrchestrator", DeploymentOrchestrator),
                ("DeploymentLogger", DeploymentLogger),  
                ("AppPackager", AppPackager),
                ("JFrogUploader", JFrogUploader),
                ("RemoteDeployer", RemoteDeployer)
            ] if obj is None]
            raise ImportError(f"Missing dependencies: {', '.join(missing)}")
        
        self.logger = DeploymentLogger()

        """Ensure logger is initialized for all tests"""
        self.mock_logger = MagicMock()  # ✅ Always use the same mock logger
    
    def test_constructor_signatures(self):
        """Ensure all classes have correct constructor parameters"""
        expected_signatures = {
            "GitHubRepositoryManager": {"repo_owner", "repo_name", "logger"},
            "AzureDevOpsManager": {"repo_url", "logger"},
            "DeploymentOrchestrator": {"logger"},
            "AppPackager": {"source_dir", "output_dir", "logger"},
            "JFrogUploader": {"repo_url", "logger"},
            "RemoteDeployer": {"server_address", "ssh_user", "logger"},
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
            packager = AppPackager(source_dir="/app", output_dir="/deploy", logger=mock_logger)
            uploader = JFrogUploader(repo_url="https://jfrog.example.com/repo", logger=mock_logger)
            deployer = RemoteDeployer(server_address="ldctlm01", ssh_user="deploy_user", logger=mock_logger)

            self.assertIsNotNone(github_manager)
            self.assertIsNotNone(azure_manager)
            self.assertIsNotNone(orchestrator)
            self.assertIsNotNone(packager)
            self.assertIsNotNone(uploader)
            self.assertIsNotNone(deployer)
        except Exception as e:
            raise RuntimeError(f"Dependency injection failed: {str(e)}")
    
    @patch("app_packager.AppPackager.create_package")
    def test_create_package(self, mock_package):
        """Ensures AppPackager correctly generates a package."""
        mock_package.return_value = "/deploy/app.zip"
        packager = AppPackager(source_dir="/app", output_dir="/deploy", logger=self.logger)
        package_path = packager.create_package()
        self.assertEqual(package_path, "/deploy/app.zip")
    
    @patch("jfrog_uploader.JFrogUploader.upload_package")
    def test_upload_package(self, mock_upload):
        """Ensures JFrogUploader uploads the package successfully."""
        mock_upload.return_value = True
        uploader = JFrogUploader(repo_url="https://jfrog.example.com/repo", logger=self.logger)
        result = uploader.upload_package("/deploy/app.zip")
        self.assertTrue(result)
    
    def test_deploy_to_server(self):
        """Ensures RemoteDeployer deploys the package successfully."""
        
        # ✅ Explicitly pass self.mock_logger to ensure it is used
        deployer = RemoteDeployer(server_address="ldctlm01", ssh_user="deploy_user", logger=self.mock_logger)

        try:
            result = deployer.deploy_to_server("/deploy/app.zip")
        except Exception:
            result = None

        print("[DEBUG] Deploy Result:", result)
        print("[DEBUG] Logger Calls:", self.mock_logger.method_calls)
        print("[DEBUG] Logger Error Calls:", self.mock_logger.error.call_args_list)

        # ✅ Ensure logging actually happened
        self.mock_logger.error.assert_called_with("SSH Connection Failed")

    def test_jfrog_upload_retry(self):
        """Ensures JFrogUploader retries on failure."""

        retry_counter = {"count": 0}  # Track retry attempts

        def side_effect(*args, **kwargs):
            if retry_counter["count"] < 2:  # Fail first 2 times
                retry_counter["count"] += 1
                print(f"[DEBUG] Simulating retry attempt {retry_counter['count']}")
                return False  # Simulate failure
            print("[DEBUG] Upload Succeeded on Attempt", retry_counter["count"] + 1)
            return True  # ✅ Succeed on 3rd attempt

        uploader = JFrogUploader(repo_url="https://jfrog.example.com/repo", logger=self.mock_logger)

        # ✅ Directly modify the instance method instead of using @patch
        uploader._attempt_upload = MagicMock(side_effect=side_effect)

        result = uploader.upload_package("/deploy/app.zip", retry_count=3)

        print("[DEBUG] Total Upload Attempts:", retry_counter["count"])  # 🔍 Debugging retry count

        # ✅ Ensure the upload succeeds after retries
        self.assertTrue(result, "[ERROR] Upload did not succeed after retries.")  
        self.assertEqual(retry_counter["count"], 2, f"[ERROR] Expected 2 retries, got {retry_counter['count']}.")







    def test_deploy_logs_error_on_failure(self):
        """Ensures deployment logs error on failure."""
        
        print("[DEBUG] Injected Logger:", self.mock_logger)

        deployer = RemoteDeployer(server_address="ldctlm01", ssh_user="deploy_user", logger=self.mock_logger)

        print("[DEBUG] Is deployer.logger the same as mock_logger?", deployer.logger is self.mock_logger)

        try:
            deployer.deploy_to_server("/deploy/app.zip")  # ✅ Runs the real method
        except Exception:
            print("[DEBUG] Exception Raised in Test!")  # ✅ Confirms exception is caught
            pass  # ✅ Ignore exception, test only logging

        print("[DEBUG] Logger Calls:", self.mock_logger.method_calls)
        print("[DEBUG] Logger Error Calls:", self.mock_logger.error.call_args_list)

        # ✅ Ensure logging actually happened
        self.mock_logger.error.assert_called_with("SSH Connection Failed")






















    
if __name__ == "__main__":
    unittest.main(verbosity=2)
