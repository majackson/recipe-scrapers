import sys
from lxml import html
from urlparse import urlparse, ParseResult
from allergy_assistant.scrapers import RecipeWebsiteScraper
from allergy_assistant.scrapers.models import ScraperRecipe, ScraperIngredient
import logging

logger = logging.getLogger("allergy_assistant.scrapers.sites.allrecipes")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class AllRecipes(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "All Recipes" 
    SOURCE_URL = "http://allrecipes.com"

    def get_recipes(self):
        """Gets a full list of recipes for this source
        Returns a list of ScraperRecipes"""
        recipe_list_url = self.SOURCE_URL + "/recipes/ViewAll.aspx"

        for page_num in xrange(1, sys.maxint):
            list_page_url = "%s?Page=%d" % (recipe_list_url, page_num)
            logger.debug("---Beginning to parse page %d" % page_num) 
            page = self.parse(list_page_url)
            if page is not None:
                for recipe in self.get_recipes_from_page(page):
                    logger.debug("found %s at %s" % (recipe.recipe_name, recipe.url) )
                    yield recipe

                if self.is_last_page(page):
                    break

    def is_last_page(self, page):
        """Determines whether this page is the last page of recipes"""
        links = page.cssselect('#ctl00_CenterColumnPlaceHolder_Pager_corePager_pageNumbers *')
        last_link = links[-1]
        return False if last_link.tag == 'a' else True

    def get_recipes_from_page(self, page):
        for recipe_row in page.cssselect('.rectable h3 a'):
            recipe_name = recipe_row.text_content()
            recipe_url = recipe_row.get('href')
            recipe = ScraperRecipe(recipe_name, source=self.SOURCE_NAME, url=recipe_url)
            yield recipe

    def parse_recipe(self, recipe):
            
        def get_ingredients():
            for ingredient in ingredients:
               ingredient = self.remove_extraneous_whitespace(ingredient.text_content())
               yield ScraperIngredient(ingredient)
       
        page = self.parse(recipe.url)
        if page is None: return None
        
        if not recipe.recipe_name:
            recipe.recipe_name = page.cssselect('.itemreviewed')[0].text_content().strip()
        recipe.source_name = self.SOURCE_NAME

        ingredients = page.cssselect('.ingredients ul li')
        recipe.add_ingredients(get_ingredients())
       
        return recipe 

def main():
    allrecipes = AllRecipes()
    allrecipes.get_and_save_all()

if __name__ == '__main__':
    main()
