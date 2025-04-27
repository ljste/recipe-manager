import db_operations
import sys

def display_menu():
    """Prints the main menu options to the console."""
    print("\n--- Recipe Database Menu ---")
    print("1. Add a New Recipe")
    print("2. List All Recipes")
    print("3. Search Recipe by Name")
    print("4. View Recipe Details")
    print("5. Exit")
    print("----------------------------")

def get_user_choice():
    """Prompts the user for menu choice and returns it."""
    while True:
        try:
            choice = input("Enter your choice (1-5): ")
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except EOFError:
             print("\nExiting.")
             sys.exit(0)
        except KeyboardInterrupt:
             print("\nExiting.")
             sys.exit(0)


def get_recipe_input():
    """Gets recipe name, description, ingredients, and instructions from the user."""
    print("\n--- Add New Recipe ---")
    while True:
        name = input("Enter Recipe Name: ").strip()
        if name:
            break
        else:
            print("Recipe name cannot be empty.")

    description = input("Enter Recipe Description (optional): ").strip()

    ingredients = []
    print("\nEnter Ingredients (type 'done' when finished):")
    while True:
        ing_name = input("  Ingredient Name: ").strip()
        if ing_name.lower() == 'done':
            if not ingredients:
                 print("Warning: No ingredients added.")
                 confirm = input("Are you sure you want to proceed without ingredients? (yes/no): ").lower()
                 if confirm != 'yes':
                     continue
            break
        if not ing_name:
            print("  Ingredient name cannot be empty.")
            continue

        while True:
            ing_quantity = input(f"  Quantity for '{ing_name}': ").strip()
            if ing_quantity:
                ingredients.append({'name': ing_name, 'quantity': ing_quantity})
                break
            else:
                print("  Quantity cannot be empty.")

    instructions = []
    print("\nEnter Instructions (one step per line, type 'done' when finished):")
    step_num = 1
    while True:
        instruction = input(f"  Step {step_num}: ").strip()
        if instruction.lower() == 'done':
            if not instructions:
                 print("Warning: No instructions added.")
                 confirm = input("Are you sure you want to proceed without instructions? (yes/no): ").lower()
                 if confirm != 'yes':
                     continue
            break 
        if instruction:
            instructions.append(instruction)
            step_num += 1
        else:
            print("  Instruction step cannot be empty.")

    return name, description, ingredients, instructions

def handle_add_recipe():
    """Handles the process of adding a new recipe."""
    name, description, ingredients, instructions = get_recipe_input()
    recipe_id = db_operations.add_recipe(name, description, ingredients, instructions)
    if recipe_id:
        print(f"\nRecipe '{name}' added successfully with ID: {recipe_id}")
    else:
        print("\nFailed to add recipe.")

def handle_list_recipes():
    """Handles listing all recipes."""
    print("\n--- All Recipes ---")
    recipes = db_operations.list_all_recipes()
    if recipes:
        for r_id, r_name in recipes:
            print(f"ID: {r_id:<5} Name: {r_name}")
    else:
        print("No recipes found in the database.")

def handle_search_recipe():
    """Handles searching for recipes by name."""
    print("\n--- Search Recipe by Name ---")
    search_term = input("Enter search term: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return

    results = db_operations.search_recipe_by_name(search_term)
    if results:
        print("\nSearch Results:")
        for r_id, r_name in results:
            print(f"ID: {r_id:<5} Name: {r_name}")
    else:
        print(f"No recipes found matching '{search_term}'.")

def handle_view_details():
    """Handles viewing the details of a specific recipe."""
    print("\n--- View Recipe Details ---")
    while True:
        try:
            recipe_id_str = input("Enter the ID of the recipe to view: ").strip()
            if not recipe_id_str:
                print("Recipe ID cannot be empty.")
                continue
            recipe_id = int(recipe_id_str)
            break
        except ValueError:
            print("Invalid ID. Please enter a number.")
        except EOFError:
             print("\nReturning to menu.")
             return
        except KeyboardInterrupt:
             print("\nReturning to menu.")
             return


    details = db_operations.get_recipe_details(recipe_id)
    if details:
        print("\n------------------------------")
        print(f"Recipe: {details['name']} (ID: {details['id']})")
        print(f"Description: {details['description'] or 'N/A'}")
        print("\nIngredients:")
        if details['ingredients']:
            for ing in details['ingredients']:
                print(f"  - {ing['name']} ({ing['quantity']})")
        else:
            print("  (No ingredients listed)")
        print("\nInstructions:")
        if details['instructions']:
            for instr in details['instructions']:
                print(f"  {instr['step']}. {instr['description']}")
        else:
            print("  (No instructions listed)")
        print("------------------------------")
    else:
        print(f"Recipe with ID {recipe_id} not found.")

def main():
    """Main function to run the recipe manager application."""
    print("Welcome to the Recipe Database Manager!")
    print("Please ensure 'database_setup.py' has been run at least once.")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            handle_add_recipe()
        elif choice == '2':
            handle_list_recipes()
        elif choice == '3':
            handle_search_recipe()
        elif choice == '4':
            handle_view_details()
        elif choice == '5':
            print("Exiting Recipe Database Manager. Goodbye!")
            break

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
