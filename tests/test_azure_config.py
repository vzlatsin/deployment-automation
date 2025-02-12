import unittest
import os
import json

class TestAzureConfig(unittest.TestCase):
    def test_load_config(self):
        """Test if config.json can be loaded correctly."""
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
        self.assertTrue(os.path.exists(config_path), "config.json is missing!")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.assertIn("AZURE_DEVOPS_PAT", config, "Missing AZURE_DEVOPS_PAT in config.json")
        except Exception as e:
            self.fail(f"Failed to read config.json: {str(e)}")

if __name__ == "__main__":
    unittest.main()
