import sys

from recipe_scrapers.utils import logger
from recipe_scrapers.scraper import RecipeWebsiteScraper

logger = logger.init("recipe_scrapers.sites.bbcgoodfood")

class BbcGoodFood(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "BBC Good Food" 
    SOURCE_URL = "http://www.bbcgoodfood.com"

    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = '#currentLetterList li h4 a'
    INGREDIENTS_SELECTOR = '#ingredients ul li'
    RECIPES_PER_PAGE = 40

    def get_recipe_list_urls(self, start_point=None):

        recipe_list_url_spec = "%s/searchAZ.do?letter=%s&pager.offset=%d"

        if start_point is None:
            letters = map(chr, range(ord('A'), ord('A')+26))
        else:
            letters = [start_point]

        for letter in letters:       
            page_offsets = xrange(0, sys.maxint, self.RECIPES_PER_PAGE)
            for page_offset in page_offsets:
                yield recipe_list_url_spec % (self.SOURCE_URL, letter, page_offset) 
                if self.is_last_page_of_letter(self.list_page):
                    break

    def is_last_page_of_letter(self, page):
        navlinks = page.cssselect('#pagesNavTop ul li a')
        return not (navlinks and navlinks[-1].text_content().strip().lower() == 'next')


def main():
    parser = BbcGoodFood.get_argparser()
    args = parser.parse_args()

    bbcgoodfood = BbcGoodFood(refresh=args.refresh)
    bbcgoodfood.get_and_save_all(start_point=args.start_point)
    
if __name__ == '__main__':
    main()
