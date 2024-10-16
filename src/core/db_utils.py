"""
This module contains utility functions for interacting with the SQLite database.
"""

import sqlite3

# Path to the schema files
SCHEMA_PATHS = ["sql/core_schema.sql",
                "sql/kit_order_schema.sql",
                "sql/assay_planning_schema.sql",
                "sql/schema.sql"]

def create_db(db_path):
    """
    db_path: str - The path to the SQLite database file.

    Create a new SQLite database with the schema defined in the schema.sql file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for schema_path in SCHEMA_PATHS:
            with open(schema_path, "r") as f:
                schema = f.read()
                cursor.executescript(schema)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

    print("Database has been created.")
    table_names = get_table_names(db_path)

    print(f"{len(table_names)} tables in the database:")
    for table_name in table_names:
        print(table_name)

def get_table_names(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    conn.close()

    return [name[0] for name in table_names]





def check_exists(db_path:str, table_name:str, conditions:dict):
    """
    db_path: str - The path to the SQLite database file.
    table_name: str - The name of the table.
    conditions: dict - A dictionary of column names and values to check if the row exists.
    """
    if not conditions:
        raise ValueError("Conditions dictionary cannot be empty.")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Build the WHERE clause based on the dictionary keys (column names)
    columns = list(conditions.keys())
    values = list(conditions.values())
    where_clause = " AND ".join([f"{col} = ?" for col in columns])

    # Dynamically create the query with placeholders for values
    query = f"SELECT id FROM {table_name} WHERE {where_clause};"

    try:
        cursor.execute(query, values)
        row = cursor.fetchone()
    except Exception as e:
        print(e)
        row = None
    finally:
        conn.close()

    return row if row else None





