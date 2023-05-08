import unittest

if __name__ == '__main__':
    # Discover and load all tests from files with the "test_*.py" pattern
    test_suite = unittest.TestLoader().discover('', pattern='test_*.py')

    # Run the tests using TextTestRunner
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
