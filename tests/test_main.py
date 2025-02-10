import subprocess
import unittest

class TestMainScript(unittest.TestCase):
    """
    Tests whether main.py correctly interprets command-line arguments
    and executes deployment steps in the correct order.
    """

    def test_main_interprets_steps_correctly(self):
        """
        Run main.py with specific steps and verify the expected output.
        """
        result = subprocess.run(
            ["python", "src/main.py", "--steps", "fetch", "compare", "push"],
            capture_output=True, text=True
        )
        
        expected_output = (
            "Executing step: fetch\n"
            "Executing step: compare\n"
            "Executing step: push\n"
        )

        self.assertEqual(result.stdout, expected_output)

if __name__ == "__main__":
    unittest.main()
