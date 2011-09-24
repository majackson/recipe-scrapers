from lxml import html
from urlparse import urlparse, ParseResult
from allergy_assistant.scrapers import RecipeWebsiteScraper
from allergy_assistant.scrapers.models import ScraperRecipe, ScraperIngredient
import logging
import argparse
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

    def __init__(self, refresh):
	self.refresh = refresh

    def get_recipes(self, start_point=None):
        """Gets a full list of recipes for this source
        Returns a list of ScraperRecipes"""
        recipe_list_url = self.SOURCE_URL + "/browse/allrecipes/"

        if start_point is None:
            letters = ['123'] + [ chr(n) for n in range(65,91) ]
        else:
            letters = [start_point]

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
                    logger.debug("Found %s" % (recipe_name)) 
                    if self.refresh or not ScraperRecipe.recipe_in_db(recipe_url):
                        recipe = ScraperRecipe(recipe_name, self.SOURCE_NAME, url=recipe_url)
                        recipe = self.parse_recipe(recipe)
                        if recipe is None:
                            next
                        else: yield recipe
                    else:
                        logger.debug("Already in db, skipping...") 
                        

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
    parser = argparse.ArgumentParser(description="Parse recipes stored at Food.com")
    parser.add_argument('--refresh', dest='refresh', action='store_true', default=False, help="Reparse urls already in database")
    parser.add_argument('--start-point', dest='start_point', default=None, help="Specify a letter or number to start parsing at")

    args = parser.parse_args()

    foodcom = FoodCom(refresh=args.refresh)
    foodcom.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
