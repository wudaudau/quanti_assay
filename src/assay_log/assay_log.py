"""
For the moment, we implement the db-related functions here.
"""

import sqlite3
import csv

from src.core.db_utils import check_exists



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



