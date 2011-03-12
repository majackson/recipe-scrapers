from allergy_assistant.parsers import RecipeWebsiteParser 
import unittest

class RecipeWebsiteParserTest(unittest.TestCase):
    
    def setUp(self):
        self.rwp = RecipeWebsiteParser() 

    def test_relative_to_absolute(self):
        
        absurl1 = "http://www.google.com"
        relurl1 = "/chrome"
        self.assertEqual( self.rwp.relative_to_absolute(absurl1, relurl1), \
                "http://www.google.com/chrome")

        absurl2 = "http://www.reddit.com/r/programming/"
        relurl2 = "comments/f2rei/"
        self.assertEqual( self.rwp.relative_to_absolute(absurl2, relurl2), \
                "http://www.reddit.com/r/programming/comments/f2rei/")

        absurl3 = "http://someurl.net/a/path"
        relurl3 = "different/path"
        self.assertEqual( self.rwp.relative_to_absolute(absurl3, relurl3), \
                "http://someurl.net/a/different/path")

    def test_postparse_save(self):
        test_recipe = ('a delicious crispy roast chicken with garlic',
            ['fresh raw chicken', 'yellow lemon', 'bunch of rosemary', '4 garlic cloves'],
            'some source')

        result = self.rwp.postparse(test_recipe)

        self.assertEqual(result, \
            ('chicken with garlic',
            ['chicken', 'lemon', 'rosemary', 'garlic cloves'],
            'some source'))



    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
