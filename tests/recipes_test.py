import unittest
from recipes import RecipeManager


class TestRecipes(unittest.TestCase):

    def test_get_recipe_data_for_ingredient(self):
        recipe_manager = RecipeManager()
        test_ingredient = 'potato'
        recipe_data = recipe_manager.get_recipes_by_ingredient(test_ingredient)
        # Assume that there is at least one recipe
        self.assertGreater(len(recipe_data), 0)
        # Assert that at least one recipe contains the test ingredient in its title
        try:
            next(filter(lambda recipes: test_ingredient in recipes['recipe']['label'], recipe_data))
        except StopIteration:
            self.fail('Test ingredient not in any of the recipe titles')


if __name__ == '__main__':
    unittest.main()