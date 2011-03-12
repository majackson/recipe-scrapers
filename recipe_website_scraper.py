
import logging
from urlparse import urlparse, ParseResult
from allergy_assistant import models
#from nltk.corpus import wordnet

class RecipeWebsiteScraper(object):

    def __init__(self):
        self.source, created = models.Source.objects.get_or_create(source_name=self.SOURCE_NAME)
        self.source.source_url = self.SOURCE_URL
        self.source.save()
    
    def relative_to_absolute(self, start_path, relative_url):
        """converts a relative url at a specified (absolute) location
        :param: start_path - the absolute path from which the relative url is being accessed
        :param: relative_url - the relative url on the page"""
        parsed_start_url = urlparse(start_path)
        new_path = '/'.join(parsed_start_url.path.split('/')[:-1] + [ relative_url ] )
        parsed_abs_url = ParseResult(scheme=parsed_start_url.scheme, netloc=parsed_start_url.netloc, \
                                path=new_path, params=parsed_start_url.params, query=parsed_start_url.query, \
                                fragment=parsed_start_url.fragment)


        return parsed_abs_url.geturl()


    def remove_extraneous_whitespace(self, string):
       return " ".join(filter(lambda i: not i.isspace(), string.split()))


    def save(self, recipe):
        recipe.parse_self()

        dish, created = models.Dish.objects.get_or_create(dish_name = recipe.recipe_name )
        dish.save()
        db_recipe, created = models.Recipe.objects.get_or_create(dish=dish, source=self.source)
        if created:
            db_recipe.url = recipe.url

        for r_ingredient in recipe.ingredients:
            db_ingredient, created = models.Ingredient.objects.get_or_create(ingredient_name = r_ingredient.ingredient_name )
            db_ingredient.save()
            db_recipe.ingredients.add(db_ingredient)

        db_recipe.save()

    def get_recipe_list(self):
        """override me"""
        return [] #recipes

    def parse_recipe(self):
        """override me"""
        return ("", [], "") #recipe name, ingredients, source name
    
    def get_all_recipes(self):
        for recipe_name, recipe_url in self.get_recipe_list():
            try:
                recipe = self.parse_recipe(recipe_url, recipe_name) 
                yield recipe
            except IOError:
                continue

    def get_and_save_all(self):
        if getattr(self, 'ENABLED', False):
            for recipe in self.get_all_recipes():
                self.save(recipe)

    @classmethod
    def get_and_save_all_sources(cls):
        for SiteParser in cls.__subclasses__():
            SiteParser().get_and_save_all()

