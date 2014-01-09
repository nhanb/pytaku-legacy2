import unittest
import sites

kissurl = 'http://kissmanga.com/Manga/Shingeki-no-Kyojin/Attack-on-Titan' \
    '-053----Faith-in-his-Idiots?id=184784'


class TestSitesInit(unittest.TestCase):

    def setUp(self):
        pass

    def testGetSite(self):
        obj = sites.get_site(kissurl)
        self.assertIsInstance(obj, sites.kissmanga.KissManga)

if __name__ == '__main__':
    unittest.main()
