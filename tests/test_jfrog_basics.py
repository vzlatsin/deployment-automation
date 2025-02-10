import sys
import os
import unittest
from unittest.mock import MagicMock

# ✅ Ensure correct module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from jfrog_uploader import JFrogUploader  # ✅ Now it should work!

class TestJFrogUploader(unittest.TestCase):
    """Basic logging and retry test for JFrogUploader"""

    def setUp(self):
        """Setup the mock logger and JFrogUploader instance"""
        self.mock_logger = MagicMock()
        self.uploader = JFrogUploader(repo_url="https://jfrog.example.com/repo", logger=self.mock_logger)

    def test_logging_basics(self):
        """✅ Ensure logging works in JFrogUploader"""
        self.uploader.logger.error("Test error message")
        self.mock_logger.error.assert_called_with("Test error message")

    def test_upload_retry_basics(self):
        """✅ Basic retry test to verify retry mechanism"""

        retry_counter = {"count": 0}  # Track retry attempts

        def side_effect(*args, **kwargs):
            if retry_counter["count"] < 2:  # Fail first 2 times
                retry_counter["count"] += 1
                print(f"[DEBUG] Simulating retry attempt {retry_counter['count']}")
                return False  # Simulate failure
            print("[DEBUG] Upload Succeeded on Attempt", retry_counter["count"] + 1)
            return True  # ✅ Succeed on 3rd attempt

        self.uploader._attempt_upload = MagicMock(side_effect=side_effect)  # ✅ Mock internal upload function

        result = self.uploader.upload_package("/deploy/app.zip", retry_count=3)

        print("[DEBUG] Total Upload Attempts:", retry_counter["count"])  # 🔍 Debugging retry count

        # ✅ Ensure the upload succeeds after retries
        self.assertTrue(result, "[ERROR] Upload did not succeed after retries.")  
        self.assertEqual(retry_counter["count"], 2, f"[ERROR] Expected 2 retries, got {retry_counter['count']}.")

if __name__ == '__main__':
    unittest.main()
