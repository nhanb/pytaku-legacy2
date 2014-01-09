#!/usr/bin/python
import optparse
import sys
import os
# Install the Python unittest package before you run this script.
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Add project root to PATH
    test_path = os.path.dirname(__file__)
    sys.path.append(os.path.dirname(test_path))

    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    #if len(args) != 2:
        #print 'Error: Exactly 2 arguments required.'
        #parser.print_help()
        #sys.exit(1)

    SDK_PATH = os.environ.get('GAE_PATH',
                              os.path.expanduser('~/google_appengine'))
    TEST_PATH = os.path.dirname(__file__)
    main(SDK_PATH, TEST_PATH)
