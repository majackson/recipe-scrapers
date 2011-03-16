from nltk.corpus import wordnet

class ScraperModel():

    name_fields = []

    @staticmethod
    def is_adjective_and_not_noun(word):
        defs = wordnet.synsets(word)
        word_is = lambda ss, wt: any(s.lexname.startswith(wt) for s in ss)
        return not (word_is(defs, 'noun') or not word_is(defs, 'adj'))

    @staticmethod
    def parse_name(name):
        PREPOSITIONS = ('of', 'to', 'in')
        MEASUREMENTS = ('g', 'mg', 'kg', 'l', 'ml', 'cl', 'grams', 'milligrams', 
                        'millilitres' , 'milliliters', 'litres', 'liters', 'centiliters',
                        'centilitres', 
                        'tsp', 'tspn', 'tbsp', 'tbspn', 'teaspoon', 'tablespoon', 
                        'bunch', 'sprinkle')
        COOKING_WORDS = ('delicious', 'tasty', 'quick', 'yummy')

        name = name.replace("&", "and")
        name = name.lower() #for processing

        words = name.split()
        #words = filter(lambda w: not is_adjective_and_not_noun(w), words)
        words = filter(lambda w: len(w) > 1, words)
        words = filter(lambda w: not w.isdigit(), words)
        #words = filter(lambda w: w not in PREPOSITIONS, words)
        words = filter(lambda w: w not in MEASUREMENTS, words)
        words = filter(lambda w: w not in COOKING_WORDS, words)
        words = filter(lambda l: l is not "!", words)

        words = filter(lambda l: bool(l), words) #filter out items which have now been reduced to empty strings
        

        return " ".join(words).title()
    

    @staticmethod
    def clip(string):
        """clips string to 255 chars (db column length)"""
        return string[:255]

    def parse_self(self):
        """Parses scraped data, removes odd formatting, measurements, anything else which shouldn't be there"""
        #override me!
        pass

class ScraperRecipe(ScraperModel):
    "Class to hold the raw recipe data scraped from websites"
    
    def __init__(self, recipe_name, source='unknown', url='unknown'):
        self.recipe_name = recipe_name
        self.source = source
        self.url = url
        self.ingredients = []

    def add_ingredient(self, ingredient):
        """Adds a single ingredient to the list of ingredients"""
        scraper_ingredient = ScraperIngredient(ingredient)
        self.ingredients.append(scraper_ingredient)

    def add_ingredients(self, ingredients):
        """Adds multiple ingredients to the list of ingredients"""
        for ingredient in ingredients:
            self.add_ingredient(ingredient)
    
    def parse_self(self):
        """Parses scraped data, removes odd formatting, measurements, anything else which shouldn't be there"""
        self.recipe_name = self.parse_name(self.recipe_name)
        self.recipe_name = self.clip(self.recipe_name)
        for ingredient in self.ingredients:
            ingredient.parse_self()
    

class ScraperIngredient(ScraperModel):
    "Class to hold the raw ingredients data scraped from websites"
    
    def __init__(self, ingredient_name):
        self.ingredient_name = ingredient_name
    
    def parse_self(self):
        """Parses scraped data, removes odd formatting, measurements, anything else which shouldn't be there"""
        self.ingredient_name = self.parse_name(self.ingredient_name)
        self.ingredient_name = self.clip(self.ingredient_name)