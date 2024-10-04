"""
For the moment, we implement the db-related functions here.
"""

import sqlite3
import csv

from src.core.db_utils import check_exists
from src.core.db_utils import get_or_insert_species


def get_or_insert_project(db_path, project_name:str, species:str, description:str):
    """
    Get or insert a project in the database.
    """
    # TODO: do we need to check validity of the data type?
     
    species_id = get_or_insert_species(db_path, species)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "project", {"name": project_name})

    if row:
        project_id = row[0]
    else:
        cursor.execute("INSERT INTO project (name, species_id, description) VALUES (?,?,?)", (project_name, species_id, description))
        project_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return project_id

def add_project_from_file(db_path): 
            
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/project.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            project_name = row["project"]
            species = row["species"]
            description = row["description"]
            project_id = get_or_insert_project(db_path, project_name, species, description)

    conn.commit()
    conn.close()


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

def add_assay_from_file(db_path): # TODO: Do we still need this function?
        
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


# TODO: get_or_insert_project_assay()
def get_or_insert_project_assay(db_path, project_name:str, assay_name:str):
    # TODO: I don't know if it is better to use the project_id and assay_id or the project_name and assay_name
        # The idea to insert into a table is basically to use HUMAN READABLE NAMES
    project_id = get_or_insert_project(db_path, project_name, None, None) # TODO: Optimise this with a wrapper function or something better
    assay_id = get_or_insert_assay(db_path, assay_name, None, None) # TODO: Optimise this with a wrapper function or something better

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "project_assay", {"project_id": project_id, "assay_id": assay_id})

    if row:
        project_assay_id = row[0]
    else:
        cursor.execute("INSERT INTO project_assay (project_id, assay_id) VALUES (?,?);", (project_id, assay_id))
        project_assay_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return project_assay_id


# TODO: add_project_assay_from_file()
def add_project_assay_from_file(db_path):
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/project_assay.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            project_name = row["project"]
            species = row["species"]
            assay_name = row["assay_name"]
            assay_type = row["assay_type"]

            project_id = get_or_insert_project(db_path, project_name, species, None)
            assay_id = get_or_insert_assay(db_path, assay_name, species, assay_type)
            project_assay_id = get_or_insert_project_assay(db_path, project_name, assay_name)

    conn.commit()
    conn.close()