import sys

from recipe_scrapers.scraper import RecipeWebsiteScraper

class AllRecipes(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "All Recipes" 
    SOURCE_URL = "http://allrecipes.com"

    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = ".grid-result-cntnr .recipe-info p a.title"
    INGREDIENTS_SELECTOR = '.ingredient-wrap li label .ingredient_name'

    def get_recipe_list_urls(self, start_point=None):
        recipe_list_url_spec = "%s/recipes/main.aspx?evt19=1&st=t&p34=HR_SortByTitle&Page=%d"

        for page_num in xrange(1, sys.maxint):
            yield recipe_list_url_spec % (self.SOURCE_URL, page_num)
            if self.is_last_page(self.list_page):
                break

    def is_last_page(self, page):
        """Determines whether this page is the last page of recipes"""
        if page:
            linkselector = '#ctl00_CenterColumnPlaceHolder_RecipeContainer_ucPager_corePager_pageNumbers *' 
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
