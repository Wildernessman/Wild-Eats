import os
import random
from typing import List, Dict, Tuple, Set

# Funny cooking instructions and responses
FUNNY_RESPONSES = {
    "instructions": [
        "Throw ingredients at the wall and see what sticks",
        "Dance with the ingredients until they're properly mixed",
        "Sing a lullaby to the dish while it cooks",
        "Ask your pet for cooking advice",
        "Meditate with your ingredients for inner cooking peace",
        "Whisper sweet nothings to your vegetables",
        "Juggle the ingredients (cooking experience required)",
        "Do the hokey pokey and turn the ingredients about",
        "Tell your ingredients a bedtime story",
        "Practice interpretive dance while stirring",
        "Give your ingredients a motivational speech",
        "Challenge your ingredients to a staring contest",
        "Perform a ritual rain dance around the cooking pot",
        "High-five each ingredient before using",
        "Name each ingredient and become their friend",
        "Teach your ingredients to tango",
        "Host a talent show for your ingredients",
        "Have a philosophical debate with your spices",
        "Form a support group for shy vegetables",
        "Organize a speed dating event for your ingredients"
    ],
    "cooking_times": [
        "Until the moon turns blue",
        "Three episodes of your favorite show",
        "Until your pet approves",
        "As long as it takes to learn juggling",
        "When the ingredients start singing back",
        "Until you can recite the alphabet backwards",
        "Two unicorn sneezes and a rainbow",
        "When pigs fly (approximately 42 minutes)",
        "Until your kitchen appliances stage an intervention",
        "As long as it takes to count to infinity (minus one)"
    ],
    "difficulty_levels": [
        "Rocket Science",
        "Blindfolded Expert",
        "Kitchen Ninja",
        "Culinary Comedian",
        "Professional Chaos",
        "Cooking Wizard",
        "Master of Disaster",
        "Kitchen Philosopher",
        "Food Whisperer",
        "Certified Food Therapist"
    ],
    "cooking_tips": [
        "Best served while doing a handstand",
        "Warning: May cause spontaneous dance parties",
        "Chef's note: Don't let your ingredients see you cry",
        "Caution: Side effects may include uncontrollable laughter",
        "Tip: Best enjoyed while wearing a superhero cape",
        "Note: Results may vary based on moon phase",
        "Warning: May attract hungry unicorns",
        "Best prepared during a full moon while howling",
        "Success rate increases with silly hat wearing",
        "Chef's secret: The food can sense your fear"
    ],
    "title_prefixes": [
        "Ridiculously",
        "Catastrophically",
        "Magically",
        "Outrageously",
        "Suspiciously",
        "Hilariously",
        "Mysteriously",
        "Dramatically",
        "Chaotically",
        "Absurdly"
    ]
}

# Existing categories and databases
INGREDIENT_CATEGORIES = {
    "proteins": {"chicken", "beef", "pork", "tofu", "fish", "shrimp", "eggs", "turkey", "bacon", "sausage", "ham", "tuna"},
    "grains": {"rice", "pasta", "quinoa", "bread", "noodles", "flour", "oats", "tortilla", "couscous", "barley"},
    "vegetables": {"carrots", "peas", "onions", "broccoli", "spinach", "tomatoes", "bell peppers", "garlic", "lettuce", "cucumber", "potatoes", "mushrooms", "zucchini", "celery"},
    "dairy": {"cheese", "milk", "cream", "yogurt", "butter", "sour cream", "parmesan", "mozzarella"},
    "seasonings": {"salt", "pepper", "soy sauce", "herbs", "spices", "curry powder", "cumin", "paprika", "oregano", "basil", "thyme"}
}

COOKING_METHODS = {
    "rice": ["fried", "curry", "casserole", "soup", "bowl"],
    "pasta": ["marinara", "alfredo", "baked", "stir-fried"],
    "chicken": ["grilled", "fried", "baked", "stir-fried", "curry"],
    "beef": ["grilled", "stir-fried", "braised", "bowl"]
}

ESSENTIAL_INGREDIENTS = {
    "proteins": 3.0,
    "grains": 2.0,
    "vegetables": 1.5,
    "dairy": 1.2,
}

PRIORITY_COMBINATIONS = {
    ("chicken", "rice"): 2.0,
    ("beef", "rice"): 1.8,
    ("pasta", "tomatoes"): 1.8,
}

# Recipe database
RECIPE_DATABASE = {
    "chicken_fried_rice": {
        "title": "Classic Chicken Fried Rice",
        "ingredients": ["chicken", "rice", "eggs", "carrots", "peas", "onions", "garlic", "soy sauce"],
        "instructions": [
            "Cook rice according to package instructions and let it cool",
            "Cut chicken into small cubes and season with salt and pepper",
            "Heat oil in a wok or large skillet over medium-high heat",
            "Cook chicken until golden brown, then remove and set aside",
            "Scramble eggs in the same pan, then remove",
            "Stir-fry vegetables until tender",
            "Add cooked rice, chicken, and eggs back to the pan",
            "Season with soy sauce and stir-fry until well combined"
        ],
        "cooking_time": "30 minutes",
        "difficulty": "medium",
        "servings": "4",
        "cuisine": "Asian"
    },
    # ... [previous recipe database entries remain unchanged]
}

def get_ingredient_category(ingredient: str) -> str:
    """Determine the category of an ingredient."""
    try:
        for category, ingredients in INGREDIENT_CATEGORIES.items():
            if ingredient.lower() in ingredients:
                return category
        return "other"
    except Exception as e:
        print(f"Error categorizing ingredient {ingredient}: {str(e)}")
        return "other"

def calculate_match_score(recipe_ingredients: Set[str], user_ingredients: Set[str]) -> Tuple[float, Set[str]]:
    """Calculate a weighted match score between recipe and user ingredients."""
    try:
        score = 0
        matched_ingredients = set()
        
        recipe_ingredients = {ing.lower() for ing in recipe_ingredients}
        user_ingredients = {ing.lower() for ing in user_ingredients}
        
        # Priority combinations check
        for (ing1, ing2), multiplier in PRIORITY_COMBINATIONS.items():
            if ing1 in user_ingredients and ing2 in user_ingredients:
                if ing1 in recipe_ingredients and ing2 in recipe_ingredients:
                    score += multiplier
                    matched_ingredients.add(ing1)
                    matched_ingredients.add(ing2)
        
        # Category and direct matches
        for recipe_ing in recipe_ingredients:
            recipe_category = get_ingredient_category(recipe_ing)
            if recipe_category != "other":
                category_ingredients = INGREDIENT_CATEGORIES[recipe_category]
                matching_category_ingredients = category_ingredients.intersection(user_ingredients)
                if matching_category_ingredients:
                    weight = ESSENTIAL_INGREDIENTS.get(recipe_category, 1.0)
                    score += weight * 0.5
                    matched_ingredients.update(matching_category_ingredients)
            
            if recipe_ing in user_ingredients:
                category = get_ingredient_category(recipe_ing)
                weight = ESSENTIAL_INGREDIENTS.get(category, 1.0)
                score += weight * 2
                matched_ingredients.add(recipe_ing)
        
        total_possible_score = sum(ESSENTIAL_INGREDIENTS.get(get_ingredient_category(ing), 1.0) * 2
                                for ing in recipe_ingredients)
        match_percentage = (score / total_possible_score) * 100 if total_possible_score > 0 else 0
        
        return match_percentage, matched_ingredients
    except Exception as e:
        print(f"Error calculating match score: {str(e)}")
        return 0, set()

def find_matching_recipes(ingredients: List[str]) -> List[Dict]:
    """Find recipes that match the given ingredients."""
    try:
        matching_recipes = []
        user_ingredients = set(ing.lower() for ing in ingredients)
        
        # Priority matches
        priority_matches = []
        for recipe_id, recipe in RECIPE_DATABASE.items():
            recipe_ingredients = set(ing.lower() for ing in recipe["ingredients"])
            for (ing1, ing2), multiplier in PRIORITY_COMBINATIONS.items():
                if ing1 in user_ingredients and ing2 in user_ingredients:
                    if ing1 in recipe_ingredients and ing2 in recipe_ingredients:
                        match_percentage, matched_ingredients = calculate_match_score(recipe_ingredients, user_ingredients)
                        match_percentage *= multiplier
                        recipe_copy = recipe.copy()
                        recipe_copy["match_percentage"] = match_percentage
                        recipe_copy["matched_ingredients"] = list(matched_ingredients)
                        priority_matches.append(recipe_copy)
        
        # Other matches
        for recipe_id, recipe in RECIPE_DATABASE.items():
            if not any(pm["title"] == recipe["title"] for pm in priority_matches):
                recipe_ingredients = set(ing.lower() for ing in recipe["ingredients"])
                match_percentage, matched_ingredients = calculate_match_score(recipe_ingredients, user_ingredients)
                
                if match_percentage >= 10:
                    recipe_copy = recipe.copy()
                    recipe_copy["match_percentage"] = match_percentage
                    recipe_copy["matched_ingredients"] = list(matched_ingredients)
                    matching_recipes.append(recipe_copy)
        
        all_matches = priority_matches + matching_recipes
        all_matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        return all_matches[:8]  # Return top 8 matches
    except Exception as e:
        print(f"Error finding matching recipes: {str(e)}")
        return []

def generate_creative_recipe(ingredients: List[str]) -> Dict:
    """Generate a humorous creative recipe."""
    try:
        main_ingredient = next((ing for ing in ingredients 
                              if get_ingredient_category(ing) in ["proteins", "grains"]), 
                             ingredients[0])
        
        # Generate funny title
        prefix = random.choice(FUNNY_RESPONSES["title_prefixes"])
        secondary = random.choice([ing for ing in ingredients if ing != main_ingredient]) if len(ingredients) > 1 else ""
        title = f"{prefix} {main_ingredient.title()}"
        if secondary:
            title += f" Dancing with {secondary.title()}"
        
        # Generate funny instructions
        instructions = [
            f"Prepare for culinary chaos with: {', '.join(ingredients)}",
            random.choice(FUNNY_RESPONSES["instructions"]),
            random.choice(FUNNY_RESPONSES["instructions"]),
            f"Make the {main_ingredient} feel special by {random.choice(FUNNY_RESPONSES['instructions']).lower()}",
            "Season with laughter and a pinch of chaos"
        ]
        
        # Add random cooking tip
        cooking_tip = random.choice(FUNNY_RESPONSES["cooking_tips"])
        
        return {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "cooking_time": random.choice(FUNNY_RESPONSES["cooking_times"]),
            "difficulty": random.choice(FUNNY_RESPONSES["difficulty_levels"]),
            "servings": f"{random.randint(2, 8)} brave souls",
            "match_percentage": 0,
            "cuisine": "Chaotic Fusion",
            "cooking_tip": cooking_tip
        }
    except Exception as e:
        print(f"Error generating creative recipe: {str(e)}")
        return {
            "title": "Emergency Food Creation",
            "ingredients": ingredients,
            "instructions": ["Mix everything together and hope for the best"],
            "cooking_time": "Until it looks edible",
            "difficulty": "Survival Mode",
            "servings": "??",
            "match_percentage": 0,
            "cuisine": "Panic Cuisine",
            "cooking_tip": "Best served with eyes closed"
        }

def generate_recipe(ingredients: List[str]) -> Tuple[Dict, List[Dict]]:
    """Generate recipes based on provided ingredients."""
    if not ingredients:
        raise Exception("Please provide at least one ingredient")
    
    try:
        matching_recipes = find_matching_recipes(ingredients)
        
        if matching_recipes:
            main_recipe = matching_recipes[0]
            return main_recipe, matching_recipes[1:6]
        
        # Generate creative recipes with humor
        creative = generate_creative_recipe(ingredients)
        alt_recipes = []
        if len(ingredients) > 2:
            for _ in range(3):
                subset = random.sample(ingredients, min(3, len(ingredients)))
                alt_recipes.append(generate_creative_recipe(subset))
        
        return creative, alt_recipes
        
    except Exception as e:
        print(f"Error in generate_recipe: {str(e)}")
        raise
