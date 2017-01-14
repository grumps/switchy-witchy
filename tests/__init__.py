import unittests


def run_tests():
    test_loader = unittests.TestLoader()
    test_suite = test_loader.discover("test", pattern="test_*.py")
