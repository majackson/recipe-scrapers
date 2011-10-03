from lxml import html
from urlparse import urlparse, ParseResult
from allergy_assistant.scrapers import RecipeWebsiteScraper
from allergy_assistant.scrapers.models import ScraperRecipe, ScraperIngredient
import logging
import argparse
import sys

class FoodChannel(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "Food Channel" 
    SOURCE_URL = "http://www.foodchannel.com"

    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = '.recipe-result a'
    INGREDIENTS_SELECTOR = '#ingredients_list li'

    def get_recipe_list_urls(self, start_point=None):
        recipe_list_url_spec = '%s/recipes/?page=%d'
        
        if start_point:
            page_numbers = [start_point]
        else:
            page_numbers = xrange(1, sys.maxint)

        for recipe_list_url in [ recipe_list_url_spec % (self.SOURCE_URL, x) for x in page_numbers ]:
            yield recipe_list_url
            if self.is_last_page():
                break

    def is_last_page(self, page):
        next_button = page.cssselect('.next')
        return False if next_button.tag == 'a' else True

def main():
    parser = argparse.ArgumentParser(description="Parse recipes stored at foodchannel.com")
    parser.add_argument('--refresh', dest='refresh', action='store_true', default=False, help="Reparse urls already in database")
    parser.add_argument('--start-point', dest='start_point', default=None, help="Specify a letter or number to start parsing at")

    args = parser.parse_args()

    foodchannel = FoodChannel(refresh=args.refresh)
    foodchannel.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
