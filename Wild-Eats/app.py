import os
from flask import Flask, render_template, request, jsonify
from recipe_generator import generate_recipe

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-recipe', methods=['POST'])
def create_recipe():
    try:
        ingredients = request.form.getlist('ingredients[]')
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
        
        main_recipe, alternative_recipes = generate_recipe(ingredients)
        
        return render_template('recipe.html', 
                             recipe=main_recipe, 
                             alternative_recipes=alternative_recipes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
