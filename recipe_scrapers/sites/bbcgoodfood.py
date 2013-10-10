import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper

class BbcGoodFood(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "BBC Good Food" 
    SOURCE_URL = "http://www.bbcgoodfood.com"

    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = '.node-recipe .node-title a'
    INGREDIENTS_SELECTOR = '#recipe-ingredients ul li'

    def get_recipe_list_urls(self, start_point=None):

        recipe_list_url_spec = "%s/search/recipes/?query=&page=%d"

        for page_num in xrange(0, sys.maxint):
            yield recipe_list_url_spec % (self.SOURCE_URL, page_num) 
            if self.is_last_page(self.list_page):
                break

    def is_last_page(self, page):
        if page is not None:
            return bool(page.cssselect('.page404'))

        return True


def main():
    parser = BbcGoodFood.get_argparser()
    args = parser.parse_args()

    bbcgoodfood = BbcGoodFood(refresh=args.refresh)
    bbcgoodfood.get_and_save_all(start_point=args.start_point)
    
if __name__ == '__main__':
    main()
