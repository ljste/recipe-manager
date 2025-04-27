import sqlite3
import os

DATABASE_FILE = 'recipes.db'

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file
    :param db_file: database file path
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite version: {sqlite3.sqlite_version}")
        print(f"Successfully connected to {db_file}")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print(f"Successfully executed: {create_table_sql.split('(')[0].strip()}")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def setup_database():
    """Sets up the database by creating tables."""

    sql_create_recipes_table = """
    CREATE TABLE IF NOT EXISTS Recipes (
        RecipeID INTEGER PRIMARY KEY AUTOINCREMENT,
        RecipeName TEXT UNIQUE NOT NULL COLLATE NOCASE, -- COLLATE NOCASE for case-insensitive unique check
        Description TEXT
    );
    """

    sql_create_ingredients_table = """
    CREATE TABLE IF NOT EXISTS Ingredients (
        IngredientID INTEGER PRIMARY KEY AUTOINCREMENT,
        IngredientName TEXT UNIQUE NOT NULL COLLATE NOCASE -- COLLATE NOCASE for case-insensitive unique check
    );
    """

    sql_create_instructions_table = """
    CREATE TABLE IF NOT EXISTS Instructions (
        InstructionID INTEGER PRIMARY KEY AUTOINCREMENT,
        RecipeID INTEGER NOT NULL,
        StepNumber INTEGER NOT NULL,
        StepDescription TEXT NOT NULL,
        FOREIGN KEY (RecipeID) REFERENCES Recipes (RecipeID) ON DELETE CASCADE -- Cascade delete if recipe is deleted
    );
    """

    sql_create_recipe_ingredients_table = """
    CREATE TABLE IF NOT EXISTS RecipeIngredients (
        RecipeIngredientID INTEGER PRIMARY KEY AUTOINCREMENT,
        RecipeID INTEGER NOT NULL,
        IngredientID INTEGER NOT NULL,
        Quantity TEXT NOT NULL,
        FOREIGN KEY (RecipeID) REFERENCES Recipes (RecipeID) ON DELETE CASCADE, -- Cascade delete if recipe is deleted
        FOREIGN KEY (IngredientID) REFERENCES Ingredients (IngredientID), -- Don't cascade delete ingredients if recipe is deleted
        UNIQUE (RecipeID, IngredientID) -- Ensure an ingredient isn't listed twice for the same recipe
    );
    """

    conn = create_connection(DATABASE_FILE)

    if conn is not None:
        print("\nCreating tables...")
        create_table(conn, sql_create_recipes_table)
        create_table(conn, sql_create_ingredients_table)
        create_table(conn, sql_create_instructions_table)
        create_table(conn, sql_create_recipe_ingredients_table)
        print("\nDatabase setup complete.")
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    if os.path.exists(DATABASE_FILE):
        print(f"Database file '{DATABASE_FILE}' already exists.")
    else:
        setup_database()
