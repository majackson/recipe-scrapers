import unittest

from recipe_scrapers.utils import urltools

class TestUrlTools(unittest.TestCase):

    def test_rel_to_abs(self):
        
        absurl1 = "http://www.google.com"
        relurl1 = "/chrome"
        self.assertEqual( urltools.rel_to_abs(absurl1, relurl1), \
                "http://www.google.com/chrome")

        absurl2 = "http://www.reddit.com/r/programming/"
        relurl2 = "comments/f2rei/"
        self.assertEqual( urltools.rel_to_abs(absurl2, relurl2), \
                "http://www.reddit.com/r/programming/comments/f2rei/")

if __name__ == '__main__':
    unittest.main()
