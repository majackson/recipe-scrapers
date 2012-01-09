import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper
from recipe_scrapers.utils import logger

logger = logger.init("recipe_scrapers.sites.foodcom")

class FoodCom(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "Food.com" 
    SOURCE_URL = "http://www.food.com"

    RELATIVE_URLS = False

    RECIPE_LINK_SELECTOR = '.bd-full ul.list a'
    INGREDIENTS_SELECTOR = '.ingredients .ingredient .name'

    def get_recipe_list_urls(self, start_point=None):
        recipe_list_url_spec = "%s/browse/allrecipes/?letter=%s&pg=%d"

        if start_point:
            letters = [start_point]
        else:
            letters = ['123'] + map(chr, range(ord('A'), ord('Z')+1))

        for letter in letters:
            for p in xrange(1, sys.maxint):
                yield recipe_list_url_spec % (self.SOURCE_URL, letter, p)
                if self.is_last_page_of_letter(self.list_page):
                    break

    def is_last_page_of_letter(self, page):
        if page:
            nextprev_buttons = page.cssselect('.nextprev')
            for button in nextprev_buttons:
                if "next" in button.text_content().lower():
                    return False
        # if nothing else returned by this point...
        return True


def main():
    parser = FoodCom.get_argparser()
    args = parser.parse_args()

    foodcom = FoodCom(refresh=args.refresh)
    foodcom.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
