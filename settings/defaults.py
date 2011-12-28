# App-wide Settings
APPLICATION_NAME = 'Allergy Assassin'
VERSION = '0.10'

LOG_PATH = '/var/log/allergy_assistant'


# Database settings
MONGO_IP = 'localhost'

ALLERGY_ASSISTANT_DB = 'allergy_assistant'

RECIPE_COLLECTION = 'recipes'
DISH_COLLECTION = 'dish'
ALLERGIES_COLLECTION = 'allergies'
REQUEST_LOG_COLLECTION = 'requests'

RESULTS_CAP = 100 #maximum number of results to search for allergen presence in

TEST_RECIPE_COLLECTION = 'test_recipes'
TEST_DISH_COLLECTION = 'test_dish'


# Web server settings
API_PORT = 8888
TEST_API_PORT = API_PORT


# Allergen Results ratings
UNKNOWN = 0
ALLERGEN_NEVER_PRESENT = 1 
ALLERGEN_RARELY_PRESENT = 2
ALLERGEN_SOMETIMES_PRESENT = 3
ALLERGEN_OFTEN_PRESENT = 4
ALLERGEN_VERY_OFTEN_PRESENT = 5

VERDICTS_TO_RATINGS = [ #verdicts supplied as 0-1, being a % of presence found
    ((0.0, 0.0), ALLERGEN_NEVER_PRESENT),
    ((0.0, 0.05), ALLERGEN_RARELY_PRESENT),
    ((0.05, 0.2), ALLERGEN_SOMETIMES_PRESENT),
    ((0.2, 0.4), ALLERGEN_OFTEN_PRESENT),
    ((0.4, 1), ALLERGEN_VERY_OFTEN_PRESENT),
]

# Autocomplete settings
DISH_AUTOCOMPLETION_MIN_SOURCES = 3  # minimum number of recipes that must exist before the recipe name appears in the autocomplete list
