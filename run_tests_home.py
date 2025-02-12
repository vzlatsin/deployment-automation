import unittest

# Discover all tests
loader = unittest.TestLoader()
suite = loader.discover('tests')

# Create a filtered test suite (excluding Azure-related tests)
suite_filtered = unittest.TestSuite()

def filter_tests(suite, filtered_suite):
    """ Recursively filter out AzureDevOpsManager tests """
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            # If it's a TestSuite, recurse into it
            filter_tests(test, filtered_suite)
        elif "AzureDevOpsManager" not in test.id():  # Now we're on a TestCase
            filtered_suite.addTest(test)

# Apply filter
filter_tests(suite, suite_filtered)

# Run the filtered test suite
runner = unittest.TextTestRunner()
runner.run(suite_filtered)
