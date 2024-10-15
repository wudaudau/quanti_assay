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

def get_or_insert_sample_type(db_path, sample_type_name:str, description:str=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "sample_type", {"name": sample_type_name})

    if row:
        sample_type_id = row[0]
    else:
        cursor.execute("INSERT INTO sample_type (name, description) VALUES (?,?);", (sample_type_name, description))
        sample_type_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return sample_type_id

def add_sample_type_from_file(db_path):
            
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/sample_type.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            sample_type_name = row["name"]
            description = row["description"]
            sample_type_id = get_or_insert_sample_type(db_path, sample_type_name, description)

    conn.commit()
    conn.close()


# TODO: get_or_insert_projects_assays()
def get_or_insert_projects_assays(db_path, project_name:str, assay_name:str, sample_type:str):
    # TODO: I don't know if it is better to use the project_id and assay_id or the project_name and assay_name
        # The idea to insert into a table is basically to use HUMAN READABLE NAMES, therefore use the names
    project_id = get_or_insert_project(db_path, project_name, None, None) # TODO: Optimise this with a wrapper function or something better
    assay_id = get_or_insert_assay(db_path, assay_name, None, None) # TODO: Optimise this with a wrapper function or something better
    sample_type_id = get_or_insert_sample_type(db_path, sample_type, None) # TODO: Optimise this with a wrapper function or something better

    # TODO: we should check if the species in the project and assay tables are the same

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = check_exists(db_path, "projects_assays", {"project_id": project_id, "assay_id": assay_id, "sample_type_id": sample_type_id})

    if row:
        projects_assays_id = row[0]
    else:
        cursor.execute("INSERT INTO projects_assays (project_id, assay_id, sample_type_id) VALUES (?,?,?);", 
                       (project_id, assay_id, sample_type_id))
        projects_assays_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return projects_assays_id


# TODO: add_projects_assays_from_file()
def add_projects_assays_from_file(db_path):
    """
    The file contains 5 columns: project, species, assay_name, assay_type, and sample_type.
    To insert into the projects_assays table, we only need the project_name, assay_name, and sample_type_name to obtain their ids.
    There should be already existing data in the species, project, sample_type, assay, and assay_type tables.
    If not, TODO: Can we raise an error to insert the missing data in the related files.
    """
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    file_path = "data/initial_data_for_the_database/projects_assays.csv"

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            project_name = row["project_name"]
            assay_name = row["assay_name"]
            sample_type = row["sample_type"]

            # project_id = get_or_insert_project(db_path, project_name, species, None) # TODO: Do we need it?
            # assay_id = get_or_insert_assay(db_path, assay_name, species, assay_type) # TODO: Do we need it?
            projects_assays_id = get_or_insert_projects_assays(db_path, project_name, assay_name, sample_type)

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




