"""
For the moment, we implement the db-related functions here.
"""

import sqlite3
import csv

from src.core.db_utils import check_exists





def get_or_insert_manufacture(db_path, manufacture_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "manufacture", {"name": manufacture_name})

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

    row = check_exists(db_path, "storage", {"name": storage_name})

    if row:
        storage_id = row[0]
    else:
        cursor.execute("INSERT INTO storage (name) VALUES (?);", (storage_name,))
        storage_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return storage_id

def get_or_insert_quanti_item_type(db_path, quanti_item_type_name:str, description:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "quanti_item_type", {"name": quanti_item_type_name})

    if row:
        quanti_item_type_id = row[0]
    else:
        cursor.execute("INSERT INTO quanti_item_type (name, description) VALUES (?,?);", (quanti_item_type_name, description))
        quanti_item_type_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return quanti_item_type_id

def get_or_insert_kit_item(db_path, kit_cat_number:str, name:str, manufacture:str, storage:str, description:str):
    manufacture_id = get_or_insert_manufacture(db_path, manufacture)
    storage_id = get_or_insert_storage(db_path, storage)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "kit_item", {"kit_cat_number": kit_cat_number})

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













