import argparse

from lxml import html

from recipe_scrapers.models import ScraperRecipe, ScraperIngredient
from recipe_scrapers import db
from recipe_scrapers.utils import logger, urltools

class RecipeWebsiteScraper(object):

    SOURCE_NAME = "Not Set"
    RELATIVE_URLS = False   # whether links on page are relative or absolute

    def __init__(self, refresh=None):
        self.refresh = refresh
        self.init_logging()

    def init_logging(self):
        self.logger = logger.init("recipe_scrapers.sites.%s" % 
            ("".join(self.SOURCE_NAME.split()).lower()))

    def clean_wspace(self, string):
        """Cleans excess whitespace in string
        "this   \n\r string\t\t123" -> "this string 123"
        """
        return " ".join(filter(lambda i: not i.isspace(), string.split())).strip()

    def get_recipes(self, start_point=None):
        """Gets a full list of recipes for this source
        Returns a list of ScraperRecipes"""
        for recipe_list_url in self.get_recipe_list_urls(start_point):
            self.list_page = self.parse(recipe_list_url)
            if self.list_page is not None:
                for recipe in self.get_recipes_from_list_page(self.list_page):
                    self.logger.debug("found %s at %s" % 
                        (recipe.recipe_name, recipe.url) )
                    if self.refresh or not ScraperRecipe.recipe_in_db(recipe.url):
                        yield recipe
                    else:
                        self.logger.debug("Recipe already in database, skipping...")
                

    def get_recipes_from_list_page(self, list_page):
        recipe_links = list_page.cssselect(self.RECIPE_LINK_SELECTOR)
        for recipe_link in recipe_links:
            recipe_name = self.format_name(recipe_link.text_content())
            recipe_href = recipe_link.get('href')
            if self.RELATIVE_URLS:
                recipe_url = urltools.rel_to_abs(self.SOURCE_URL, recipe_href)
            else:
                recipe_url = recipe_href
            recipe = ScraperRecipe(recipe_name, source=self.SOURCE_NAME, 
                                        url=recipe_url)
            yield recipe

    def format_name(self, recipe_name):
        """Optionally overridden for per-site based name formatting"""
        return recipe_name

    def parse_recipe(self, recipe):
        """Receives a recipe object containing only name source and url
        Returns same object populated with ingredients"""
        page = self.parse(recipe.url)
        if page is None: return None

        ingredients = page.cssselect(self.INGREDIENTS_SELECTOR)
        for ingredient in ingredients:
            ingredient = self.clean_wspace(ingredient.text_content())
            recipe.add_ingredient(ScraperIngredient(ingredient))
       
        return recipe 

    def get_recipe_list_urls(self, start_point):
        raise NotImplementedError("Override me!")

    def parse(self, url):
        try:    
            page = html.parse(url).getroot()
        except IOError:
            page = None
        return page

    def get_all_recipes(self, start_point=None):
        for recipe in self.get_recipes(start_point):
            try:
                if self.parse_recipe(recipe) is not None:
                    yield recipe
            except IOError:
                continue

    def get_and_save_all(self, start_point=None):
        if getattr(self, 'ENABLED', False):
            for recipe in self.get_all_recipes(start_point):
                recipe.save()
            db.ensure_indexes()


    @classmethod
    def get_and_save_all_sources(cls):
        for SiteParser in cls.__subclasses__():
            SiteParser().get_and_save_all()

    @classmethod
    def get_argparser(klass):
        parser_desc = "Parse recipes stored at %s" % klass.SOURCE_NAME
        parser = argparse.ArgumentParser(description=parser_desc)
        parser.add_argument('--refresh', 
                            dest='refresh', 
                            action='store_true', 
                            default=False, 
                            help="Reparse urls already in database")

        parser.add_argument('--start-point', 
                            dest='start_point',
                            default=None, 
                            help="Specify a letter or number to start parsing at")

        return parser

