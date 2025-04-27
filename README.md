# CSC 4480 - Recipe Database Project

This project implements a simple command-line application to manage a recipe database using Python and SQLite.

## Features

* Add new recipes, including name, description, ingredients (with quantities), and step-by-step instructions.
* Automatically adds new ingredients to a master list if they don't exist.
* List all recipes currently stored in the database.
* Search for recipes by name (case-insensitive, partial matching).
* View the full details of a specific recipe (ingredients and instructions).
* Uses SQLite for data storage in a single file (`recipes.db`).

## Project Structure

* `database_setup.py`: Script to initialize the database and create the necessary tables. Run this first.
* `db_operations.py`: Module containing all functions that interact directly with the SQLite database (CRUD operations).
* `recipe_manager.py`: The main application script that provides the user interface (command-line menu) and orchestrates calls to `db_operations.py`.
* `insert_sample_data.py`: Script to populate the database with a few sample recipes for testing and demonstration. Run this after `database_setup.py`.
* `recipes.db`: The SQLite database file (created automatically by `database_setup.py` or `recipe_manager.py` if it doesn't exist).
* `README.md`: This file.

## Prerequisites

* Python 3.x installed on your system. SQLite support (`sqlite3` module) is built into standard Python distributions, so no extra database installation is typically required.

## Setup and Execution

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ljste/recipe-manager.git
    cd recipe-manager
    ```

2.  **Set up the Database:**
    Run the setup script to create the `recipes.db` file and the tables.
    ```bash
    python database_setup.py
    ```
    *(Note: If `recipes.db` already exists, this script will print a message and exit. You can modify it or manually delete `recipes.db` if you need to recreate the tables.)*

3.  **[Optional] Insert Sample Data:**
    Run this script to add 3 sample recipes to the database.
    ```bash
    python insert_sample_data.py
    ```
    *(Note: This script uses the `add_recipe` function, so it will skip adding recipes whose names already exist in the database.)*

4.  **Run the Application:**
    Start the main recipe manager application.
    ```bash
    python recipe_manager.py
    ```

5.  **Interact with the Menu:**
    Follow the on-screen prompts to:
    * Add new recipes (you'll be guided through entering name, description, ingredients, and instructions).
    * List all existing recipes.
    * Search for recipes by name.
    * View the details of a specific recipe by entering its ID.
    * Exit the application.

## Database Schema

* **Recipes**: `RecipeID` (PK), `RecipeName` (UNIQUE NOT NULL), `Description`
* **Ingredients**: `IngredientID` (PK), `IngredientName` (UNIQUE NOT NULL)
* **Instructions**: `InstructionID` (PK), `RecipeID` (FK -> Recipes), `StepNumber` (NOT NULL), `StepDescription` (NOT NULL)
* **RecipeIngredients**: `RecipeIngredientID` (PK), `RecipeID` (FK -> Recipes), `IngredientID` (FK -> Ingredients), `Quantity` (NOT NULL), UNIQUE(`RecipeID`, `IngredientID`)
