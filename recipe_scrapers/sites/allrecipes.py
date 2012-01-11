import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper

class AllRecipes(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "All Recipes" 
    SOURCE_URL = "http://allrecipes.com"

    RELATIVE_URLS = False

    RECIPE_LINK_SELECTOR = ".rectable h3 a"
    INGREDIENTS_SELECTOR = '.ingredients ul li'

    def get_recipe_list_urls(self, start_point=None):
        recipe_list_url_spec = "%s/recipes/ViewAll.aspx?Page=%d"

        if start_point:
            page_numbers = [start_point]
        else:
            page_numbers = xrange(1, sys.maxint)

        for page_num in page_numbers:
            yield recipe_list_url_spec % (self.SOURCE_URL, page_num)
            if self.is_last_page(self.list_page):
                break

    def is_last_page(self, page):
        """Determines whether this page is the last page of recipes"""
        if page:
            linkselector = '#ctl00_CenterColumnPlaceHolder_Pager_corePager_pageNumbers *' 
            links = page.cssselect(linkselector)
            last_link = links[-1]
            if last_link.tag == 'a':
                return False
        
        # if nothing returned by this point
        return True


def main():
    parser = AllRecipes.get_argparser()
    args = parser.parse_args()

    allrecipes = AllRecipes(refresh=args.refresh)
    allrecipes.get_and_save_all(start_point=args.start_point)

if __name__ == '__main__':
    main()
