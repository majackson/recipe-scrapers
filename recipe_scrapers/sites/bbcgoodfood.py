from lxml import html
import argparse

from recipe_scrapers.utils import logger
from recipe_scrapers.scraper import RecipeWebsiteScraper
from recipe_scrapers.models import ScraperRecipe, ScraperIngredient

logger = logger.init("recipe_scrapers.sites.bbcgoodfood")

class BbcGoodFood(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "BBC Good Food" 
    SOURCE_URL = "http://www.bbcgoodfood.com"

    def __init__(self, refresh=False):
        self.refresh = refresh

    def get_recipes(self, start_point=None):
        """Gets a full list of recipes for this source
        Returns a list of ScraperRecipes"""
        root_url = "http://www.bbcgoodfood.com/"
        recipe_list_url = root_url + "searchAZ.do"
        
        def get_recipes_on_page(page_root):
            """Gets all recipes on a given parsed page
            :param: page_root lxml-parsed root element object of page containing recipe links
            
            Returns a list of ScaperRecipes in the format (recipe_name, relative_recipe_url)"""
            for recipe_link in page_root.cssselect('#currentLetterList li h4 a'):
                    recipe_name = recipe_link.text_content().strip()
                    recipe_url = recipe_link.attrib.get('href')
                    yield ScraperRecipe(recipe_name, source=self.SOURCE_NAME, \
                            url=recipe_url)

        if start_point is None:
            letters = [ chr(x) for x in range(97, 97+26) ]
        else:
            letters = [start_point]

        for letter in letters:       
            logger.debug("---Beginning to parse letter %s" % letter) 
            page = html.parse(recipe_list_url + "?letter=%s" % letter).getroot()
            pagecount = 1
            while( page is not None ): #keep getting next page #TODO make more pythonic 
                logger.debug('Parsing page %d of %s' % (pagecount, letter))
                for scraper_recipe in get_recipes_on_page(page):
                    scraper_recipe.url = self.relative_to_absolute(root_url, scraper_recipe.url) 
                    logger.debug("found %s at %s" % (scraper_recipe.recipe_name, scraper_recipe.url) )
                    if self.refresh or not ScraperRecipe.recipe_in_db(scraper_recipe.url):
                        yield scraper_recipe
                    else:
                        logger.debug("Recipe already in database, skipping")
                pages_links = page.cssselect('#pagesNavTop ul li a')
                if pages_links and pages_links[-1].text_content().strip().lower() == 'next':
                    page = html.parse(root_url + pages_links[-1].attrib.get('href')).getroot()  
                    pagecount += 1
                else:
                    page = None # move onto next letter
        
        # print recipes
        # print "\n"
        # print "Number of recipes: %d" % len(recipes)

        # return recipes
        
    def parse_recipe(self, recipe):
            
        def get_ingredients():
            for ingredient in ingredients:
               ingredient = self.remove_extraneous_whitespace(ingredient.text_content())
               yield ScraperIngredient(ingredient)
       
        page = html.parse(recipe.url).getroot() #on rare occasions this times out!
        #weird workaround to catch 99.9% of times this happens:
        if page is None:
            page = html.parse(recipe.url).getroot()

        if page is None: #on the uber-rare occasions it *still doesn't exist*, 
            raise IOError # throw exception and let caller handle it

        if not recipe.recipe_name:
            recipe.recipe_name = page.cssselect('#mainContent .out h1')[0].text_content().strip()
        recipe.source_name = self.SOURCE_NAME

        ingredients = page.cssselect('#ingredients ul li')
        recipe.add_ingredients(get_ingredients())
       
        return recipe 

def main():
    parser = argparse.ArgumentParser(description="Parse recipes stored at BBC Good Food")
    parser.add_argument('--refresh', dest='refresh', action='store_true', default=False, help="Reparse urls already in database")
    parser.add_argument('--start-point', dest='start_point', default=None, help="Specify a letter or number to start parsing at")

    args = parser.parse_args()

    bbcgoodfood = BbcGoodFood(refresh=args.refresh)
    bbcgoodfood.get_and_save_all(start_point=args.start_point)
    
if __name__ == '__main__':
    main()
