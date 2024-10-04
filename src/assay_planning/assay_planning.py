"""
For the moment, we implement the db-related functions here.
"""

import sqlite3

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