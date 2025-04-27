import sqlite3

DATABASE_FILE = 'recipes.db'

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def add_ingredient_if_not_exists(conn, ingredient_name):
    """
    Adds an ingredient to the Ingredients table if it doesn't already exist.
    Returns the IngredientID.
    Handles case-insensitivity for ingredient names.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT IngredientID FROM Ingredients WHERE IngredientName = ? COLLATE NOCASE", (ingredient_name,))
        result = cursor.fetchone()

        if result:
            return result['IngredientID']
        else:
            cursor.execute("INSERT INTO Ingredients (IngredientName) VALUES (?)", (ingredient_name,))
            conn.commit()
            print(f"Added new ingredient: {ingredient_name}")
            return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Error adding ingredient '{ingredient_name}': {e}")
        conn.rollback()
        return None
    except sqlite3.Error as e:
        print(f"Database error adding ingredient '{ingredient_name}': {e}")
        conn.rollback()
        return None

def add_recipe(recipe_name, description, ingredients_list, instructions_list):
    """
    Adds a complete recipe to the database.
    Handles adding recipe details, ingredients (checking existence),
    linking ingredients with quantities, and adding instructions.
    Returns the RecipeID if successful, None otherwise.
    """
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    recipe_id = None

    try:
        cursor.execute("INSERT INTO Recipes (RecipeName, Description) VALUES (?, ?)", (recipe_name, description))
        recipe_id = cursor.lastrowid
        print(f"\nAdding recipe '{recipe_name}' (ID: {recipe_id})...")

        print("Processing ingredients...")
        for ingredient_info in ingredients_list:
            ing_name = ingredient_info.get('name')
            ing_quantity = ingredient_info.get('quantity')

            if not ing_name or not ing_quantity:
                print(f"Skipping invalid ingredient entry: {ingredient_info}")
                continue

            ingredient_id = add_ingredient_if_not_exists(conn, ing_name)

            if ingredient_id:
                cursor.execute("""
                    INSERT INTO RecipeIngredients (RecipeID, IngredientID, Quantity)
                    VALUES (?, ?, ?)
                """, (recipe_id, ingredient_id, ing_quantity))
                print(f"  Linked: {ing_name} ({ing_quantity})")
            else:
                raise sqlite3.Error(f"Could not process ingredient: {ing_name}")

        print("Adding instructions...")
        for i, instruction_text in enumerate(instructions_list):
            step_number = i + 1
            cursor.execute("""
                INSERT INTO Instructions (RecipeID, StepNumber, StepDescription)
                VALUES (?, ?, ?)
            """, (recipe_id, step_number, instruction_text))
            print(f"  Step {step_number}: Added.")

        conn.commit()
        print(f"Successfully added recipe '{recipe_name}'!")
        return recipe_id

    except sqlite3.IntegrityError as e:
        print(f"\nError adding recipe '{recipe_name}': {e}. Recipe might already exist.")
        conn.rollback()
        return None
    except sqlite3.Error as e:
        print(f"\nDatabase error occurred while adding recipe '{recipe_name}': {e}")
        conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def list_all_recipes():
    """Retrieves and returns a list of all recipe names and IDs."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT RecipeID, RecipeName FROM Recipes ORDER BY RecipeName COLLATE NOCASE")
        recipes = cursor.fetchall()
        return [(row['RecipeID'], row['RecipeName']) for row in recipes]
    except sqlite3.Error as e:
        print(f"Error listing recipes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def search_recipe_by_name(search_term):
    """
    Searches for recipes where the name contains the search_term (case-insensitive).
    Returns a list of matching (RecipeID, RecipeName) tuples.
    """
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        query = "SELECT RecipeID, RecipeName FROM Recipes WHERE RecipeName LIKE ? COLLATE NOCASE ORDER BY RecipeName COLLATE NOCASE"
        cursor.execute(query, (f'%{search_term}%',))
        recipes = cursor.fetchall()
        return [(row['RecipeID'], row['RecipeName']) for row in recipes]
    except sqlite3.Error as e:
        print(f"Error searching recipes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_recipe_details(recipe_id):
    """
    Retrieves full details for a specific recipe ID.
    Returns a dictionary containing recipe info, ingredients, and instructions, or None if not found.
    """
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    recipe_details = {}

    try:
        cursor.execute("SELECT RecipeID, RecipeName, Description FROM Recipes WHERE RecipeID = ?", (recipe_id,))
        recipe_info = cursor.fetchone()

        if not recipe_info:
            return None

        recipe_details['id'] = recipe_info['RecipeID']
        recipe_details['name'] = recipe_info['RecipeName']
        recipe_details['description'] = recipe_info['Description']

        cursor.execute("""
            SELECT I.IngredientName, RI.Quantity
            FROM RecipeIngredients RI
            JOIN Ingredients I ON RI.IngredientID = I.IngredientID
            WHERE RI.RecipeID = ?
            ORDER BY I.IngredientName COLLATE NOCASE
        """, (recipe_id,))
        ingredients = cursor.fetchall()
        recipe_details['ingredients'] = [{'name': row['IngredientName'], 'quantity': row['Quantity']} for row in ingredients]

        cursor.execute("""
            SELECT StepNumber, StepDescription
            FROM Instructions
            WHERE RecipeID = ?
            ORDER BY StepNumber
        """, (recipe_id,))
        instructions = cursor.fetchall()
        recipe_details['instructions'] = [{'step': row['StepNumber'], 'description': row['StepDescription']} for row in instructions]

        return recipe_details

    except sqlite3.Error as e:
        print(f"Error retrieving details for recipe ID {recipe_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':

    print("\n--- All Recipes ---")
    all_recipes = list_all_recipes()
    if all_recipes:
        for r_id, r_name in all_recipes:
            print(f"ID: {r_id}, Name: {r_name}")
    else:
        print("No recipes found.")

    print("\n--- Search Results for 'Spaghetti' ---")
    search_results = search_recipe_by_name('Spaghetti')
    if search_results:
        for r_id, r_name in search_results:
            print(f"ID: {r_id}, Name: {r_name}")
    else:
        print("No matching recipes found.")

    print("\n--- Details for Recipe ID 1 ---")
    details = get_recipe_details(1)
    if details:
        print(f"Name: {details['name']}")
        print(f"Description: {details['description']}")
        print("Ingredients:")
        for ing in details['ingredients']:
            print(f"  - {ing['name']} ({ing['quantity']})")
        print("Instructions:")
        for instr in details['instructions']:
            print(f"  {instr['step']}. {instr['description']}")
    else:
        print("Recipe not found or error retrieving details.")
