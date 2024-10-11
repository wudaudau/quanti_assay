"""
For the moment, we implement the db-related functions here.
"""

import sqlite3
import csv

from src.core.db_utils import check_exists
from src.core.core_tables import get_or_insert_species


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
    """
    The file contains 4 columns: project, species, assay_name, assay_type
    Therefore, if no existing species or assay_type data is available, the function will insert them into the database.
    TODO: If there is existing data, what to do if the species or assay_type is different?
    """
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/project_assay.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            project_name = row["project_name"]
            species = row["species"]
            assay_name = row["assay_name"]
            assay_type = row["assay_type"]

            # project_id = get_or_insert_project(db_path, project_name, species, None) # TODO: Do we need it?
            # assay_id = get_or_insert_assay(db_path, assay_name, species, assay_type) # TODO: Do we need it?
            project_assay_id = get_or_insert_project_assay(db_path, project_name, assay_name)

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


















def get_or_insert_assays_analytes(db_path, assay_name:str, analyte_name:str, spot:int, opt_analyte_name:str):
    from src.assay_planning.assay_planning import get_or_insert_assay
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




