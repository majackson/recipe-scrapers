"""As more processing is done for each recipe, this script can be run to
reprocess all recipes already stored. Processing defined in scrapers/models.py"""

from allergy_assistant import db
from allergy_assistant.scrapers.models import ScraperRecipe, ScraperIngredient

def reprocess_recipe(recipe):
    recipe_model = ScraperRecipe(recipe['recipe_name'])

    recipe_model.source = recipe['source']
    recipe_model.url = recipe['_id']
    recipe_model.ingredients = [ ScraperIngredient(ingredient) \
        for ingredient in recipe['ingredients'] ]

    recipe_model.save()

def run():
    for recipe in db.recipes.find():
        reprocess_recipe(recipe)

if __name__=='__main__':
    run()
