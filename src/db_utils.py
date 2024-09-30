"""
This module contains utility functions for interacting with the SQLite database.
"""

import sqlite3
import csv


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





def check_exists(db_path:str, table_name:str, column_name, value):
    """
    db_path: str - The path to the SQLite database file.
    table_name: str - The name of the table.
    column_name: str - The name of the column.
    value: str - The value to check for in the column.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM {table_name} WHERE {column_name} = ?;", (value,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return row
    else:
        return None







def get_or_insert_manufacture(db_path, manufacture_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "manufacture", "name", manufacture_name)

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

    row = check_exists(db_path, "storage", "name", storage_name)

    if row:
        storage_id = row[0]
    else:
        cursor.execute("INSERT INTO storage (name) VALUES (?);", (storage_name,))
        storage_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return storage_id

def get_or_insert_kit_item(db_path, kit_cat_number:str, name:str, manufacture:str, storage:str, description:str):
    manufacture_id = get_or_insert_manufacture(db_path, manufacture)
    storage_id = get_or_insert_storage(db_path, storage)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "kit_item", "kit_cat_number", kit_cat_number)

    if row:
        kit_item_id = row[0]
    else:
        cursor.execute("INSERT INTO kit_item (kit_cat_number, name, manufacture_id, storage_id, description) VALUES (?,?,?,?,?);", 
                    (kit_cat_number, name, manufacture_id, storage_id, description))
        kit_item_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return kit_item_id



def add_kit_item_from_file(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/kit_item.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            kit_cat_number = row["cat_number"]
            name = row["name"]
            manufacture = row["manufacture"]
            storage = row["storage"]
            description = row["description"]
            kit_item_id = get_or_insert_kit_item(db_path, kit_cat_number, name, manufacture, storage, description)

    conn.commit()
    conn.close()











def get_or_insert_analyte(db_path, analyte_name:str):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "analyte", "name", analyte_name)

    if row:
        analyte_id = row[0]
    else:
        cursor.execute("INSERT INTO analyte (name) VALUES (?);", (analyte_name,))
        analyte_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return analyte_id

def get_or_insert_analyte_mapping(db_path, analyte_name:str, std_analyte_name:str):

    std_analyte_id = get_or_insert_analyte(db_path, std_analyte_name)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "analyte_mapping", "name", analyte_name)

    if row:
        analyte_mapping_id = row[0]
    else:
        cursor.execute("INSERT INTO analyte_mapping (name, std_analyte_id) VALUES (?,?);", (analyte_name, std_analyte_id))
        analyte_mapping_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return analyte_mapping_id
    
def add_analyte_mapping_from_file(db_path):
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/analyte_mapping.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            analyte_name = row["analyte"]
            std_analyte_name = row["std_analyte"]
            analyte_mapping_id = get_or_insert_analyte_mapping(db_path, analyte_name, std_analyte_name)

    conn.commit()
    conn.close()