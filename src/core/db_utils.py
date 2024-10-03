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











def get_or_insert_analyte(db_path, analyte_name:str):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "analyte", {"name": analyte_name})

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

    row = check_exists(db_path, "analyte_mapping", {"name": analyte_name})

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












def get_or_insert_species(db_path, species_name:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "species", {"name": species_name})

    if row:
        species_id = row[0]
    else:
        cursor.execute("INSERT INTO species (name) VALUES (?);", (species_name,))
        species_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return species_id

def get_or_insert_assay_type(db_path, assay_type_name:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "assay_type", {"name": assay_type_name})

    if row:
        assay_type_id = row[0]
    else:
        cursor.execute("INSERT INTO assay_type (name) VALUES (?);", (assay_type_name,))
        assay_type_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return assay_type_id

def get_or_insert_assay(db_path, assay_name:str, species:str, assay_type:str):
    species_id = get_or_insert_species(db_path, species)
    assay_type_id = get_or_insert_assay_type(db_path, assay_type)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "assay", {"name": assay_name})

    if row:
        assay_id = row[0]
    else:
        cursor.execute("INSERT INTO assay (name, species_id, assay_type_id) VALUES (?,?,?);", 
                    (assay_name, species_id, assay_type_id))
        assay_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return assay_id

def add_assay_from_file(db_path):
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/assay.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            assay_name = row["name"]
            species = row["species"]
            assay_type = row["assay_type"]
            assay_id = get_or_insert_assay(db_path, assay_name, species, assay_type)

    conn.commit()
    conn.close()

    

















def get_or_insert_assays_analytes(db_path, assay_name:str, analyte_name:str, spot:int, opt_analyte_name:str):
    assay_id = get_or_insert_assay(db_path, assay_name, None, None)
    analyte_id = get_or_insert_analyte(db_path, analyte_name)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "assays_analytes", {"assay_id": assay_id, 
                                                    "analyte_id": analyte_id, 
                                                    "spot": spot})

    if row:
        assays_analytes_id = row[0]
    else:
        cursor.execute("INSERT INTO assays_analytes (assay_id, analyte_id, spot, opt_analyte_name) VALUES (?,?,?,?);", 
                    (assay_id, analyte_id, spot, opt_analyte_name))
        assays_analytes_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return assays_analytes_id

def add_assays_analytes_from_file(db_path):
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/assays_analytes.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            assay_name = row["assay_name"]
            analyte_name = row["analyte_name"]
            spot = row["spot"]
            opt_analyte_name = row["opt_analyte_name"]
            assays_analytes_id = get_or_insert_assays_analytes(db_path, assay_name, analyte_name, spot, opt_analyte_name)

    conn.commit()
    conn.close()












def get_or_insert_item_lot(db_path, item_cat_number:str, lot_number:str, expiry_date:str):
    item_id = get_or_insert_kit_item(db_path, item_cat_number, None, None, None, None) # TODO: We may seperate get and insert functions

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "item_lot", {"item_id": item_id, 
                                            "lot_number": lot_number})

    if row:
        item_lot_id = row[0]
    else:
        cursor.execute("INSERT INTO item_lot (item_id, lot_number, expiry_date) VALUES (?,?,?);", 
                    (item_id, lot_number, expiry_date))
        item_lot_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return item_lot_id

def get_or_insert_sd_initial_concentration(db_path, sd_initial_concentration_name:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "sd_inital_concentration", {"name": sd_inital_concentration_name})

    if row:
        sd_inital_concentration_id = row[0]
    else:
        cursor.execute("INSERT INTO sd_inital_concentration (name) VALUES (?);", (sd_inital_concentration_name,))
        sd_inital_concentration_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return sd_inital_concentration_id