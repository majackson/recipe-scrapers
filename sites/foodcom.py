from lxml import html
from urlparse import urlparse, ParseResult
from allergy_assistant.scrapers import RecipeWebsiteScraper
from allergy_assistant.scrapers.models import ScraperRecipe, ScraperIngredient
import logging
import sys

logger = logging.getLogger("allergy_assistant.scrapers.sites.foodcom")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class FoodCom(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "Food.com" 
    SOURCE_URL = "http://www.food.com"

    def get_recipes(self):
        """Gets a full list of recipes for this source
        Returns a list of ScraperRecipes"""
        recipe_list_url = self.SOURCE_URL + "/browse/allrecipes/"

        letters = ['123'] + [ chr(n) for n in range(65,91) ]
        for letter in letters:
            for p in xrange(1, sys.maxint):
                recipe_page = recipe_list_url + "?letter=%s&pg=%d" % (letter, p)
                page = html.parse(recipe_page).getroot()

                for page in []:
                    recipe = ScraperRecipe()
                    self.parse_recipe(recipe)

                if self.is_last_page(page): break

    def is_last_page(self, page):
        pass
        
    def parse_recipe(self, recipe):
        """Receives a recipe object containing only name source and url
        Returns same object populated with ingredients"""
        pass

if __name__ == '__main__':
    foodcom = FoodCom()
    foodcom.get_and_save_all()
