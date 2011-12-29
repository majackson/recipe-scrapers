import unittest

from recipe_scrapers import settings, db
from recipe_scrapers.utils import reprocess_recipes

class TestReprocessRecipes(unittest.TestCase):

    FIXTURES = [

        {'_id': 'http://recipes.net/recipes/beef-stroganoff',
         'source': 'Recipes.net',
         'url': 'http://recipes.net/recipes/beef-stroganoff',
         'recipe_name': 'Beef Stroganoff',
         'ingredients': ['beef', 'cream', 'mushrooms', 'onions', 'rice', 'garlic'],
         'keywords': ['beef', 'stroganoff']},

        {'_id': 'http://recipes.net/recipes/beef-jerky',

         'source': 'Recipes.net',
         'url': 'http://recipes.net/recipes/beef-jerky',
         'recipe_name': 'Beef Jerky',
         'ingredients': ['beef'],
         'keywords': ['Beef', 'Jerky']},

        {'_id': 'http://food.com/recipes/spaghetti-carbonara?recipe=1#recipe',
         'source': 'Food.com',
         'url': 'http://food.com/recipes/spaghetti-carbonara?recipe=1#recipe',
         'recipe_name': 'Spaghetti Carbonara',
         'ingredients': ['spaghetti', 'cream', 'mushrooms', 'bacon', 'rosemary', 'garlic', 'oregano', 'basil']},

        {'_id': 'http://rcp.th/r/112542.html#view',
         'source': 'Thai Recipes',
         'url': 'http://rcp.th/r/112542.html#view',
         'recipe_name': 'ThAI     GreEEN curry',
         'ingredients': ['rice', 'lemongrass', 'chicken', 'onions', 'spices', 'ting'],
         'keywords': ['th', 'ai', 7]},
         

    ]
    
    def setUp(self):
        self.recipes_coll = db.db[settings.TEST_RECIPE_COLLECTION]
        reprocess_recipes.db.recipes = self.recipes_coll
        self._populate_data()

    def _populate_data(self):
        self.recipes_coll.remove()
        for doc in self.FIXTURES:
            self.recipes_coll.insert(doc)
        db.ensure_indexes()

    def test_reprocess_recipes(self):

        reprocess_recipes.run()

        # invariant 1: same number of recipes as fixtures
        self.assertEqual(self.recipes_coll.count(), len(self.FIXTURES))

        # invariant 2: has all expected keys present
        for doc in self.recipes_coll.find():
            self.assertTrue('_id' in doc.keys())
            self.assertTrue('source' in doc.keys())
            self.assertTrue('url' in doc.keys())
            self.assertTrue('recipe_name' in doc.keys())
            self.assertTrue('ingredients' in doc.keys())
            self.assertTrue('keywords' in doc.keys())

        # invariant 3: keywords all lower case
        for doc in self.recipes_coll.find():
            self.assertTrue( all([ kw.islower() for kw in doc['keywords']]) )

        # invariant 4: ingredients is a list of strings
        for doc in self.recipes_coll.find():
            self.assertTrue( isinstance(doc['ingredients'], list) )
            self.assertTrue( all([ isinstance(i, basestring) for i in doc['ingredients']]))


if __name__=='__main__':
    unittest.main()
