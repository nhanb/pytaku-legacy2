#!/usr/bin/python
import sys
import os
import unittest


def main():
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Get test path
    test_path = os.path.dirname(__file__)

    print test_path

    suite = unittest.loader.TestLoader().discover(test_path)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if (result.wasSuccessful()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
