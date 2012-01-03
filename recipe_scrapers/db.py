from recipe_scrapers import settings
from pymongo import Connection

conn = Connection(settings.MONGO_IP)
db = conn[settings.RECIPE_DB]

recipes = db[settings.RECIPE_COLLECTION] 
dish = db[settings.DISH_COLLECTION]
allergies = db[settings.ALLERGIES_COLLECTION]
requests = db[settings.REQUEST_LOG_COLLECTION]

def ensure_indexes():
    recipes.ensure_index('recipe_name')
    recipes.ensure_index('keywords')
