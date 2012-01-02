from recipe_scrapers.scraper import RecipeWebsiteScraper
from recipe_scrapers.models import ScraperIngredient
from recipe_scrapers.utils import logger

logger = logger.init("recipe_scrapers.sites.epicurious")

class Epicurious(RecipeWebsiteScraper):

    ENABLED = True
    SOURCE_NAME = "epicurious" 
    SOURCE_URL = "http://www.epicurious.com"

    RELATIVE_URLS = True

    RECIPE_LINK_SELECTOR = '#recipe_main .sr_rows .sr_lnk_box a'
    INGREDIENTS_SELECTOR = '#ingredients'

    def get_recipe_list_urls(self, start_point=None):
        recipe_lists = []
        recipe_lists.append('%s/tools/searchresults?type=simple&threshold=53&att=122&pageNumber=1&pageSize=6000&resultOffset=0' % \
            self.SOURCE_URL)

        recipe_lists.append('%s/tools/searchresults/members?type=simpleMember&threshold=53&att=122&pageNumber=1&pageSize=6000&resultOffset=0' % \
            self.SOURCE_URL)
        
        for recipe_list in recipe_lists:
            yield recipe_list

    def parse_recipe(self, recipe):
        """Receives a recipe object containing only name source and url
        Returns same object populated with ingredients"""
        page = self.parse(recipe.url)
        if page is None: return None

        ingredients_text = page.cssselect(self.INGREDIENTS_SELECTOR)[0].text_content()
        ingredients_text = ingredients_text.replace("<h2>Ingredients</h2>", "")
        ingredients = ingredients_text.split("<br>")

        for ingredient in ingredients:
            ingredient = self.remove_extraneous_whitespace(ingredient)
            recipe.add_ingredient(ScraperIngredient(ingredient))
       
        return recipe 


def main():
    parser = Epicurious.get_argparser()
    args = parser.parse_args()

    epicurious = Epicurious(refresh=args.refresh)
    epicurious.get_and_save_all(args.start_point)

if __name__ == '__main__':
    main()
