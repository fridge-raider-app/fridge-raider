import requests
from config import EDAMAM_APP_ID, EDAMAM_APP_KEY


class RecipeManager:

    def __init__(self):
        self.app_id = EDAMAM_APP_ID
        self.app_key = EDAMAM_APP_KEY

    def get_recipes_by_ingredient(self, ingredient):
        try:
            recipes = requests.get(f'https://api.edamam.com/search?q={ingredient}&app_id={self.app_id}&app_key={self.app_key}')
            information = recipes.json()
            return information.get('hits')[:6]
        except (requests.exceptions.RequestException, TypeError):
            return []

    def get_recipes_by_extended_query(self, ingredient, diet=None, health=None, cuisine_type=None, meal_type=None):
        try:
            url = f'https://api.edamam.com/search?q={ingredient}&app_id={self.app_id}&app_key={self.app_key}'
            if diet:
                url += f'&diet={diet}'
            if health:
                url += f'&health={health}'
            if cuisine_type:
                url += f'&cuisineType={cuisine_type}'
            if meal_type:
                url += f'&mealType={meal_type}'
            recipes = requests.get(url)
            information = recipes.json()
            return information.get('hits')[:6]
        except (requests.exceptions.RequestException, TypeError, AttributeError):
            return []
