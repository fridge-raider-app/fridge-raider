from database.connection import get_db_connection


def add_favourite_recipe(user_id, name, source, url, image_url):
    """
    Adds a new recipe to a particular user's favourites.
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""INSERT INTO user_favourites (user_id, recipe_name, recipe_source, recipe_url, image_url)
                            VALUES (%s, %s, %s, %s, %s)""", [user_id, name, source, url, image_url])
            connection.commit()


def get_favourite_recipes(user_id):
    """
    Retrieves all favourite recipes for a particular user.
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT id, recipe_name, recipe_source, recipe_url, image_url
                            FROM user_favourites
                            WHERE user_id = %s""", [user_id])
            results = cursor.fetchall()
            return results


def remove_favourite_recipe(id, user_id):
    """
    Removes a recipe from a particular user's favourites.
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""DELETE FROM user_favourites 
                            WHERE id = %s AND user_id = %s""", [id, user_id])
            connection.commit()
