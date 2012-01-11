
import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper

class FoodNetwork(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "Food Network" 
    SOURCE_URL = "http://www.foodnetwork.com"
    
    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = '.idxlist li a'
    INGREDIENTS_SELECTOR = '.kv-ingred-list1 .ingredient'

    def get_recipe_list_urls(self, start_point=None):
        recipe_list_url_spec = "%s/food/about_us/index/0,1000854,FOOD_32959_93219_%s-%d,00.html"
        if start_point:
            letters = [start_point]
        else:
            letters = [''] + map(chr, range(ord('A'),ord('A')+26))

        for letter in letters:
            page_numbers = xrange(1, sys.maxint)
            for page_number in page_numbers:
                yield recipe_list_url_spec % (self.SOURCE_URL, letter, page_number)
                if self.is_last_page_of_letter(self.list_page):
                    break


    def is_last_page_of_letter(self, page):
        if page:
            disabled_buttons = page.cssselect('.pglnks .dis span')
            for button in disabled_buttons:
                if "next" in button.text_content().lower():
                    return False
        # if nothing else returned by this point...
        return True
        
    def format_name(self, recipe_name):
        return self.remove_parens_name(recipe_name)

    def remove_parens_name(self, recipe_name):
        """On this site some (maybe 50%) of recipes name the celebrity chef
        who came up with the recipes, in the format "blah blah (captain blah)".
        These must be stripped out"""
        return recipe_name.split(' (')[0]

def main():
    parser = FoodNetwork.get_argparser()
    args = parser.parse_args()

    foodnetwork = FoodNetwork(refresh=args.refresh)
    foodnetwork.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
