import argparse
import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper
from recipe_scrapers.models import ScraperRecipe, ScraperIngredient
from recipe_scrapers.utils import logger

logger = logger.init("recipe_scrapers.sites.foodnetwork")

class FoodNetwork(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "Food Network" 
    SOURCE_URL = "http://www.foodnetwork.com"

    def __init__(self, refresh):
	self.refresh = refresh

    def get_recipes(self, start_point=None):
        """Gets a full list of recipes for this source
        Returns a list of ScraperRecipes"""
        recipe_list_url = self.SOURCE_URL + "/food/about_us/index/0,1000854,FOOD_32959_93219_%s-%d,00.html"

        if start_point is None:
            letters = [''] + [ chr(n) for n in range(65,91) ]
        else:
            letters = [start_point]

        for letter in letters:
            logger.debug("---Beginning to parse letter %s" % letter) 
            for p in xrange(1, sys.maxint):
                logger.debug("-----Parsing page %d of '%s'" % (p, letter)) 
                recipe_page = recipe_list_url % (letter, p)
                page = self.parse(recipe_page)
                if page is None: next

                for recipe_link in page.cssselect('.idxlist li a'):
                    recipe_name = recipe_link.text_content().strip()
                    recipe_name = self.remove_parens_name(recipe_name)
                    recipe_url = self.relative_to_absolute(self.SOURCE_URL, recipe_link.get('href'))
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
        disabled_buttons = page.cssselect('.pglnks .dis span')
        for button in disabled_buttons:
            if "next" in button.text_content().lower():
                return False
        # if nothing else returned by this point...
        return True
        
    def parse_recipe(self, recipe):
        """Receives a recipe object containing only name source and url
        Returns same object populated with ingredients"""
        page = self.parse(recipe.url)
        if page is None: return None

        ingredients = page.cssselect('.kv-ingred-list1 .ingredient')
        for ingredient in ingredients:
            ingredient = self.remove_extraneous_whitespace(ingredient.text_content())
            recipe.add_ingredient(ScraperIngredient(ingredient))
       
        return recipe 

    def remove_parens_name(self, recipe_name):
        """On this site some (maybe 50%) of recipes name the celebrity chef
        who came up with the recipes, in the format "blah blah (captain blah)".
        These must be stripped out"""
        return recipe_name.split(' (')[0]

def main():
    parser = argparse.ArgumentParser(description="Parse recipes stored at Food.com")
    parser.add_argument('--refresh', dest='refresh', action='store_true', default=False, help="Reparse urls already in database")
    parser.add_argument('--start-point', dest='start_point', default=None, help="Specify a letter or number to start parsing at")

    args = parser.parse_args()

    foodnetwork = FoodNetwork(refresh=args.refresh)
    foodnetwork.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
