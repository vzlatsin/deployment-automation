import unittest
import sys

if __name__ == "__main__":
    loader = unittest.TestLoader()

    # Allow running specific tests (optional argument)
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        suite = loader.loadTestsFromName(test_name)
    else:
        suite = loader.discover("tests")

    runner = unittest.TextTestRunner()
    runner.run(suite)
