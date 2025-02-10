import sys
import os
import unittest
from unittest.mock import MagicMock

# ✅ Ensure correct module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from remote_deployer import RemoteDeployer  # Ensure this works

class TestRemoteDeployer(unittest.TestCase):
    """Basic logging test for RemoteDeployer"""

    def setUp(self):
        """Setup the mock logger and RemoteDeployer instance"""
        self.mock_logger = MagicMock()
        self.deployer = RemoteDeployer(server_address="ldctlm01", ssh_user="deploy_user", logger=self.mock_logger)

    def test_logging_basics(self):
        """✅ Existing working test (Unmodified)"""
        self.deployer.logger.error("Test error message")
        self.mock_logger.error.assert_called_with("Test error message")

    def test_deploy_logs_error_reproduction(self):
        """✅ New test: Recreate the failing test from test_deployment_automation.py"""
        try:
            self.deployer.deploy_to_server("/deploy/app.zip")
        except Exception:
            pass  # ✅ Allow exception, focus on logging

        print("[DEBUG] Logger Calls:", self.mock_logger.method_calls)
        print("[DEBUG] Logger Error Calls:", self.mock_logger.error.call_args_list)

        # ✅ Ensure logging actually happened
        self.mock_logger.error.assert_called_with("SSH Connection Failed")

if __name__ == '__main__':
    unittest.main()
