#!/usr/bin/python
import sys
import os
import unittest


if __name__ == '__main__':

    # Add project root to PATH
    test_path = os.path.dirname(__file__)
    proj_path = os.path.dirname(test_path)
    sys.path.append(proj_path)

    # Add SDK path to, well, PATH
    sdk_path = os.environ.get(
        'GAE_PATH',  # read environment variable if available
        proj_path + '/google_appengine'  # gae path on travis
    )
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)
