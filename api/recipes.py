import requests


class RecipeManager:

    def __init__(self):
        self.app_id = 'd8af5172'
        self.app_key = 'bb1f673c949cedf5dace0c4f9376f520'

    def get_recipes_by_ingredient(self, ingredient):
        recipes = requests.get(f'https://api.edamam.com/search?q={ingredient}&app_id={self.app_id}&app_key={self.app_key}')
        information = recipes.json()
        return information.get('hits')
