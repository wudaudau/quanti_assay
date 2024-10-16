"""
It's a module that contains the core tables of the database.
"""

import sqlite3
import csv

from src.core.db_utils import check_exists

# It's a module that contains the core tables of the database.
# We need to prevent import functions from the submodules to avoid circular imports.

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

