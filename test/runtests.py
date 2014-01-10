#!/usr/bin/python
import os
import unittest


def main():
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Get test path
    test_path = os.path.dirname(__file__)

    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
