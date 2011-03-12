from lxml import html
from urlparse import urlparse, ParseResult
from allergy_assistant.scrapers import RecipeWebsiteScraper
from allergy_assistant.scrapers.models import ScraperRecipe, ScraperIngredient
import logging

import logging

logger = logging.getLogger("allergy_assistant.parsers.sites.bbcgoodfood")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class BbcGoodFood(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "BBC Good Food" 
    SOURCE_URL = "http://www.bbcgoodfood.com"

    def get_recipe_list(self):
        """Gets a full list of recipes for this source
        Returns a list of recipes in the format (recipe, recipe_url) """
        root_url = "http://www.bbcgoodfood.com/"
        recipe_list_url = root_url + "searchAZ.do"
        recipes = []
        
        def get_recipes_on_page(page_root):
            """Gets all recipes on a given parsed page
            :param: page_root lxml-parsed root element object of page containing recipe links
            
            Returns a list of recipes in the format (recipe_name, relative_recipe_url)"""
            for recipe_link in page_root.cssselect('#currentLetterList li h4 a'):
                    yield (recipe_link.text_content().strip(), recipe_link.attrib.get('href'))

        start_letter_code = 97
        for letter_code in range(start_letter_code, start_letter_code+26):       
            letter = chr(letter_code)
            logger.debug("---Beginning to parse letter %s" % letter) 
            page = html.parse(recipe_list_url + "?letter=%s" % letter).getroot()
            pagecount = 1
            while( page is not None ): #keep getting next page #TODO make more pythonic 
                logger.debug('Parsing page %d of %s' % (pagecount, letter))
                for recipe_title, relative_recipe_url in get_recipes_on_page(page):
                    recipe_url = self.relative_to_absolute(root_url, relative_recipe_url) 
                    logger.debug("found %s at %s" % (recipe_title, recipe_url) )
                    yield (recipe_title, recipe_url)
                pages_links = page.cssselect('#pagesNavTop ul li a')
                if pages_links and pages_links[-1].text_content().strip().lower() == 'next':
                    page = html.parse(root_url + pages_links[-1].attrib.get('href')).getroot()  
                    pagecount += 1
                else:
                    page = None #move onto next letter
        
        #print recipes
        #print "\n"
        #print "Number of recipes: %d" % len(recipes)

        #return recipes
        
    def parse_recipe(self, recipe_url, recipe_name=None):
            
        def get_ingredients():
            for ingredient in ingredients:
               yield self.remove_extraneous_whitespace(ingredient.text_content())
       
        page = html.parse(recipe_url).getroot() #on rare occasions this times out!
        #weird workaround to catch 99.9% of times this happens:
        if page is None:
            page = html.parse(recipe_url).getroot()

        if page is None: #on the uber-rare occasions it *still doesn't exist*, 
            raise IOError # throw exception and let caller handle it

        if not recipe_name:
            recipe_name = page.cssselect('#mainContent .out h1')[0].text_content().strip()
        recipe  = ScraperRecipe(recipe_name)
        recipe.source_name = self.SOURCE_NAME
        recipe.url = recipe_url

        ingredients = page.cssselect('#ingredients ul li')
        recipe.add_ingredients(get_ingredients())
       
        return recipe 


if __name__ == '__main__':
    bbcgoodfood = BbcGoodFood()
    #r = bbcgoodfood.parse_recipe('http://www.bbcgoodfood.com/recipes/1089637/sweet-potato-and-spinach-bake')
    #print (r[0], [i for i in r[1]], r[2])
