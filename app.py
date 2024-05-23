from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_BASE_URL = "https://ayur-analytics-6mthurpbxq-el.a.run.app/get"
PLACEHOLDER_IMAGE_URL = "/static/placeholder_image.jpg"  # Path to placeholder image

favorites = []

@app.route('/')
def index():
    try:
        response = requests.get(f"{API_BASE_URL}/all")
        response.raise_for_status()
        data = response.json()
        recipes = data.get('recipesList', [])  # Extract the list of recipes
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipes: {e}")
        recipes = []
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<name>')
def recipe_detail(name):
    try:
        response = requests.get(f"{API_BASE_URL}/{name}")
        response.raise_for_status()
        recipe_data = response.json()
        
        # Check if image URL is valid, if not, replace it with placeholder image URL
        image_url = recipe_data.get('foodImage', PLACEHOLDER_IMAGE_URL) if recipe_data.get('foodImage') else PLACEHOLDER_IMAGE_URL
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipe details for {name}: {e}")
        # Render custom error page for non-existent recipe names
        return render_template('error.html', message="Recipe not found."), 404

    # Extracting relevant data from the recipe data
    recipe_details = {
        'name': recipe_data.get('foodName', ''),
        'image': image_url,
        'description': recipe_data.get('foodDescription', ''),
        'ingredients': recipe_data.get('keyIngredients', [])
    }

    return render_template('detail.html', recipe=recipe_details)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    name = request.form.get('name')
    image = request.form.get('image')
    description = request.form.get('description')

    # Create a favorite recipe dictionary
    favorite_recipe = {
        'name': name,
        'image': image,
        'description': description
    }
    
    # Avoid duplicates
    if favorite_recipe not in favorites:
        favorites.append(favorite_recipe)
    
    return redirect(url_for('favorites_page'))

@app.route('/favorites')
def favorites_page():
    print(f"Current favorites: {favorites}")  # Debug print
    return render_template('favorites.html', favorites=favorites)

if __name__ == "__main__":
    app.run(debug=True)
