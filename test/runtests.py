#!/usr/bin/python
import sys
import os
import unittest
import dev_appserver


if __name__ == '__main__':

    # Obligatory GAE crap
    dev_appserver.fix_sys_path()

    # Get test path
    test_path = os.path.dirname(__file__)

    # Run all tests in the test path
    suite = unittest.loader.TestLoader().discover(test_path)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Exit with appropriate code so travis can detect failures correctly
    if (result.wasSuccessful()):
        sys.exit(0)
    else:
        sys.exit(1)
