import os
import unittest

# load all hidden markov model unit tests
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# search for all hidden markov model unittests in the corresponding directory
test_dir = os.path.dirname(__file__) + r"/simulated-learning-paths/"
tests = loader.discover(start_dir=test_dir, pattern="test_*.py")

# add tests to suite
suite.addTests(tests)

# run test suite
runner = unittest.TextTestRunner()
runner.run(suite)
