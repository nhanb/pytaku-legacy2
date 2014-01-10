import unittest
import sites
from google.appengine.ext import testbed


class TestSitesInit(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_site(self):
        obj = sites.get_site(kissurl)
        self.assertIsInstance(obj, sites.kissmanga.Kissmanga)

        obj = sites.get_site('http://nerdyweekly.com/blah')
        self.assertIsNone(obj)

    # sites.get_html() is too trivial to test, since it's only a thin wrapper
    # of the most basic urlfetch usage


class TestKissmanga(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

        self.chapter_html = sites.get_html(kissurl)

    def test_get_pages(self):
        pass
        # TODO: finish test cases for this

if __name__ == '__main__':
    unittest.main()


kissurl = 'http://kissmanga.com/Manga/Shingeki-no-Kyojin/Attack-on-Titan' \
    '-053----Faith-in-his-Idiots?id=184784'
