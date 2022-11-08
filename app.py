from flask import Flask, flash, request, render_template, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

from config import SECRET_KEY

from database.users import add_user, email_available, get_user_with_credentials, get_user_by_id
from database.favourites import add_favourite_recipe, get_favourite_recipes, remove_favourite_recipe
from api.recipes import RecipeManager

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.login_message = 'Please log in to view this page.'
login_manager.login_message_category = 'error'

recipe_manager = RecipeManager()


class User(UserMixin):

    def __init__(self, user_details):
        self.id = user_details.get('id')
        self.username = user_details.get('username')
        self.email = user_details.get('email')


@login_manager.user_loader
def user_loader(user_id):
    user_details = get_user_by_id(user_id)
    if user_details is None:
        return None
    user = User(user_details)
    return user


@app.get('/')
def view_home():
    return render_template("home.html", user=current_user)


@app.get('/about')
def view_about():
    return render_template("about.html", user=current_user)


@app.get('/faq')
def view_faq():
    return render_template("faq.html", user=current_user)


@app.get('/search')
def view_recipe_search():
    ingredient = request.args.get("ingredient") or ""
    if ingredient:
        recipes = recipe_manager.get_recipes_by_ingredient(ingredient)
    else:
        recipes = None
    return render_template("search.html", user=current_user, recipes=recipes, ingredient=ingredient)


@app.get('/login')
def view_login():
    if not current_user.is_anonymous:
        return redirect('/fridge')
    return render_template("login.html", user=current_user)


@app.post('/login')
def submit_login():
    if not current_user.is_anonymous:
        return redirect('/fridge')
    email = request.form.get('email')
    password = request.form.get('password')
    user = get_user_with_credentials(email, password)
    if user is None:
        flash("Invalid credentials.", 'error')
    else:
        user = User(user)
        login_user(user)
        return redirect('/fridge')
    return redirect('/login')


@app.get('/signup')
def view_signup():
    if not current_user.is_anonymous:
        return redirect('/fridge')
    return render_template("signup.html", user=current_user)


@app.post('/signup')
def submit_signup():
    if not current_user.is_anonymous:
        return redirect('/fridge')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if len(password) < 8:
        flash("Passwords should be at least 8 characters long.", 'error')
    elif not email_available(email):
        flash("An account with that email already exists.", 'error')
    else:
        add_user(username, email, password)
        flash("New account created.", 'info')
        return redirect('/login')
    return redirect('/signup')


@app.post('/logout')
@login_required
def submit_logout():
    logout_user()
    return redirect('/')


@app.get('/fridge')
@login_required
def view_fridge():
    ingredient = request.args.get("ingredient") or ""
    diet = request.args.get("diet") or ""
    health = request.args.get("health") or ""
    cuisine_type = request.args.get("cuisine_type") or ""
    meal_type = request.args.get("meal_type") or ""
    if ingredient:
        recipes = recipe_manager.get_recipes_by_extended_query(ingredient, diet, health, cuisine_type, meal_type)
    else:
        recipes = None
    return render_template("fridge.html", user=current_user, recipes=recipes, round=round,
                           ingredient=ingredient, diet=diet, health=health, cuisine_type=cuisine_type, meal_type=meal_type)


@app.get('/favourites')
@login_required
def view_favourites():
    recipes = get_favourite_recipes(current_user.id)
    return render_template("favourites.html", user=current_user, recipes=recipes)


@app.post('/favourites/add')
@login_required
def add_favourite():
    recipe_name = request.form.get('recipe_name')
    recipe_source = request.form.get('recipe_source')
    recipe_url = request.form.get('recipe_url')
    image_url = request.form.get('image_url')
    add_favourite_recipe(current_user.id, recipe_name, recipe_source, recipe_url, image_url)
    return redirect('/favourites')


@app.post('/favourites/remove')
@login_required
def remove_favourite():
    recipe_id = request.form.get('recipe_id')
    remove_favourite_recipe(recipe_id, current_user.id)
    return redirect('/favourites')


if __name__ == '__main__':
    app.run()
