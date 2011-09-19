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
            logger.debug("---Beginning to parse letter %s" % letter) 
            for p in xrange(1, sys.maxint):
                logger.debug("-----Parsing page %d of '%s'" % (p, letter)) 
                recipe_page = recipe_list_url + "?letter=%s&pg=%d" % (letter, p)
                page = self.parse(recipe_page)
                if page is None: next

                for recipe_link in page.cssselect('.bd-full ul.list a'):
                    recipe_name = recipe_link.text_content().strip()
                    recipe_url = recipe_link.get('href')
                    recipe = ScraperRecipe(recipe_name, self.SOURCE_NAME, url=recipe_url)
                    logger.debug("Found %s" % (recipe_name)) 
                    recipe = self.parse_recipe(recipe)
                    if recipe is None:
                        next
                    else: yield recipe

                if self.is_last_page_of_letter(page): break

    def is_last_page_of_letter(self, page):
        nextprev_buttons = page.cssselect('.nextprev')
        for button in nextprev_buttons:
            if "next" in button.text_content().lower():
                return False
        # if nothing else returned by this point...
        return True
        
    def parse_recipe(self, recipe):
        """Receives a recipe object containing only name source and url
        Returns same object populated with ingredients"""
        page = self.parse(recipe.url)
        if page is None: return None

        ingredients = page.cssselect('.ingredients .ingredient .name')
        for ingredient in ingredients:
            ingredient = self.remove_extraneous_whitespace(ingredient.text_content())
            recipe.add_ingredient(ScraperIngredient(ingredient))
       
        return recipe 

def main():
    foodcom = FoodCom()
    foodcom.get_and_save_all()

if __name__ == '__main__':
    main()
