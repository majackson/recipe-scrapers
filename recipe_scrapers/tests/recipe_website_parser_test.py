import unittest

from recipe_scrapers.scraper import RecipeWebsiteScraper

class RecipeWebsiteScraperTest(unittest.TestCase):
    
    def setUp(self):
        self.rws = RecipeWebsiteScraper() 

    def test_postparse_save(self):
        test_recipe = ('a delicious crispy roast chicken with garlic',
            ['fresh raw chicken', 'yellow lemon', 'bunch of rosemary', '4 garlic cloves'],
            'some source')

        result = self.rws.postparse(test_recipe)

        self.assertEqual(result, \
            ('chicken with garlic',
            ['chicken', 'lemon', 'rosemary', 'garlic cloves'],
            'some source'))



    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
