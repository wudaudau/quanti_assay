"""
This module contains utility functions for interacting with the SQLite database.
"""

import sqlite3



# Path to the schema.sql file
SCHEMA_PATH = "sql/schema.sql"

def create_db(db_path):
    """
    db_path: str - The path to the SQLite database file.

    Create a new SQLite database with the schema defined in the schema.sql file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        with open(SCHEMA_PATH, "r") as f:
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

def get_or_insert_manufacture(db_path, manufacture_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM manufacture WHERE name = ?;", (manufacture_name,))
    row = cursor.fetchone()

    if row:
        manufacture_id = row[0]
    else:
        cursor.execute("INSERT INTO manufacture (name) VALUES (?);", (manufacture_name,))
        manufacture_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return manufacture_id

def get_or_insert_storage(db_path, storage_name):
    # TODO: We will deal with the description later

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    cursor.execute("SELECT id FROM storage WHERE name = ?;", (storage_name,))
    row = cursor.fetchone()

    if row:
        storage_id = row[0]
    else:
        cursor.execute("INSERT INTO storage (name) VALUES (?);", (storage_name,))
        storage_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return storage_id


def add_kit_item_from_file(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/kit_item.csv"

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                cursor.execute("INSERT INTO kit_item (name) VALUES (?);", (line,))

    conn.commit()
    conn.close()