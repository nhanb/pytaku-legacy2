import unittest
import sites
from google.appengine.ext import testbed


class TestSitesInit(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

    def test_get_site(self):
        obj = sites.get_site(kissurl)
        self.assertIsInstance(obj, sites.kissmanga.Kissmanga)

        obj = sites.get_site('http://nerdyweekly.com/blah')
        self.assertIsNone(obj)

    def test_get_html(self):
        cases = [
            ['', None],
            ['asdf', None],
            ['@#sdf%123"', None],
            # TODO: add success cases
        ]

        for url, expected in cases:
            result = sites.get_html(url)
            if expected is None:
                self.assertIsNone(result)
            else:
                self.assertEqual(expected)


class TestKissmanga(unittest.TestCase):

    #def setUp(self):
        #self.testbed = testbed.Testbed()
        #self.testbed.activate()
        #self.testbed.init_urlfetch_stub()

        #self.chapter_html = sites.get_html(kissurl)

    def test_get_pages(self):
        pass
        # TODO: finish test cases for this

if __name__ == '__main__':
    unittest.main()


kissurl = 'http://kissmanga.com/Manga/Shingeki-no-Kyojin/Attack-on-Titan' \
    '-053----Faith-in-his-Idiots?id=184784'
