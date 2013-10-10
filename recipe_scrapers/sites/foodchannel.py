import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper

class FoodChannel(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "Food Channel" 
    SOURCE_URL = "http://www.foodchannel.com"

    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = '.recipes .tile_content h2 a'
    INGREDIENTS_SELECTOR = '#ingredients li'

    def get_recipe_list_urls(self, start_point=None):
        recipe_list_url_spec = '%s/recipes/?page=%d'
        
        if start_point:
            page_numbers = [start_point]
        else:
            page_numbers = xrange(1, sys.maxint)

        for page_number in page_numbers:
            yield recipe_list_url_spec % (self.SOURCE_URL, page_number)
            if self.is_last_page(self.list_page):
                break

    def is_last_page(self, page):
        if page is None:  # will be none if previous page num 404'd
            return True

def main():
    parser = FoodChannel.get_argparser()
    args = parser.parse_args()

    foodchannel = FoodChannel(refresh=args.refresh)
    foodchannel.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
