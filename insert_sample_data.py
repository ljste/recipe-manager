import db_operations

recipe1 = {
    'name': 'Classic Pancakes',
    'description': 'Fluffy pancakes perfect for breakfast.',
    'ingredients': [
        {'name': 'All-Purpose Flour', 'quantity': '1 1/2 cups'},
        {'name': 'Baking Powder', 'quantity': '3 1/2 tsp'},
        {'name': 'Salt', 'quantity': '1 tsp'},
        {'name': 'White Sugar', 'quantity': '1 tbsp'},
        {'name': 'Milk', 'quantity': '1 1/4 cups'},
        {'name': 'Egg', 'quantity': '1'},
        {'name': 'Butter', 'quantity': '3 tbsp, melted'}
    ],
    'instructions': [
        'In a large bowl, sift together the flour, baking powder, salt and sugar.',
        'Make a well in the center and pour in the milk, egg and melted butter; mix until smooth.',
        'Heat a lightly oiled griddle or frying pan over medium high heat.',
        'Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.',
        'Brown on both sides and serve hot.'
    ]
}

recipe2 = {
    'name': 'Simple Guacamole',
    'description': 'Easy and quick guacamole dip.',
    'ingredients': [
        {'name': 'Avocado', 'quantity': '3 ripe'},
        {'name': 'Lime', 'quantity': '1, juiced'},
        {'name': 'Salt', 'quantity': '1 tsp'},
        {'name': 'Onion', 'quantity': '1/2 cup, diced'},
        {'name': 'Cilantro', 'quantity': '3 tbsp, chopped'},
        {'name': 'Tomato', 'quantity': '2 roma, diced'},
        {'name': 'Garlic', 'quantity': '1 clove, minced'},
        {'name': 'Cayenne Pepper', 'quantity': '1 pinch (optional)'}
    ],
    'instructions': [
        'Cut avocados in half, remove pit and scoop out flesh into a mixing bowl.',
        'Gently mash the avocado with a fork.',
        'Add lime juice and salt, stir to combine.',
        'Stir in onion, cilantro, tomatoes, and garlic.',
        'Add cayenne pepper if desired.',
        'Serve immediately with tortilla chips.'
    ]
}

recipe3 = {
    'name': 'Basic Omelette',
    'description': 'A fundamental omelette recipe.',
    'ingredients': [
        {'name': 'Egg', 'quantity': '2 large'},
        {'name': 'Milk', 'quantity': '2 tbsp'},
        {'name': 'Salt', 'quantity': 'Pinch'},
        {'name': 'Black Pepper', 'quantity': 'Pinch'},
        {'name': 'Butter', 'quantity': '1 tsp'},
        {'name': 'Cheese', 'quantity': '1/4 cup, shredded (optional)'},
        {'name': 'Ham', 'quantity': '2 tbsp, diced (optional)'}
    ],
    'instructions': [
        'Whisk eggs, milk, salt, and pepper in a small bowl until blended.',
        'Heat butter in a nonstick skillet over medium-high heat until hot.',
        'Pour egg mixture into skillet. Eggs should set immediately at edges.',
        'Gently push cooked portions from edges toward the center with inverted turner so that uncooked eggs can reach the hot pan surface.',
        'Continue cooking, tilting pan and gently moving cooked portions as needed.',
        'When top surface of eggs is thickened and no visible liquid egg remains, place filling (cheese, ham, etc.) on one side of the omelette.',
        'Fold omelette in half with turner. Slide onto plate.',
        'Serve immediately.'
    ]
}


sample_recipes = [recipe1, recipe2, recipe3]

def insert_samples():
    """Inserts the defined sample recipes into the database."""
    print("--- Inserting Sample Recipes ---")
    print("Note: If a recipe name already exists, it will be skipped.")

    added_count = 0
    skipped_count = 0

    for recipe_data in sample_recipes:
        print("-" * 20)
        recipe_id = db_operations.add_recipe(
            recipe_data['name'],
            recipe_data['description'],
            recipe_data['ingredients'],
            recipe_data['instructions']
        )
        if recipe_id:
            added_count += 1
        else:
            skipped_count += 1

    print("\n--- Sample Data Insertion Summary ---")
    print(f"Successfully added: {added_count} recipes")
    print(f"Skipped (already exist or error): {skipped_count} recipes")
    print("-" * 35)

if __name__ == '__main__':

    insert_samples()

