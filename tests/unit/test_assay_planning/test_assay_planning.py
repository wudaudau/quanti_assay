# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.assay_planning.assay_planning import * # The code to test
import unittest # The test framework

import os
import tempfile

from src.core.db_utils import create_db

class TestAssayPlanning(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for the SQLite database
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        # TODO: Using in-memory database should be a better option
            # However, it seems that the connection is closes after each function so the database is lost.

    def tearDown(self):
        # Close and remove the temporary file after the test
        self.db_file.close()
        os.unlink(self.db_file.name)

    def test_get_or_insert_project(self):
        create_db(self.db_path)

        project_name, species, description = ["CE-PSY (IF)", "Human", "FACE-SZ"]
        project_id = get_or_insert_project(self.db_path, project_name, species, description)
        self.assertEqual(project_id, 1)

        project_id = get_or_insert_project(self.db_path, project_name, species, description)
        self.assertEqual(project_id, 1)

    def test_add_project_from_file(self):
        create_db(self.db_path)

        add_project_from_file(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project;")
        res = cursor.fetchall()
        conn.close()

        self.assertEqual(len(res), 13)
        self.assertTupleEqual(res[0], (1, 'CE-PSY (IF)', 1, 'FACE-SZ'))
        self.assertTupleEqual(res[1], (2, 'BIOFACE-PSY', 1, 'FACE-BD and FACE-DR'))
        self.assertTupleEqual(res[6], (7, 'CANDY_MOUSE', 2, '')) # TODO: '' or None?

    def test_get_or_insert_assay_type(self):
        create_db(self.db_path)

        assay_type_name = "ELISA"
        assay_type_id = get_or_insert_assay_type(self.db_path, assay_type_name)
        self.assertEqual(assay_type_id, 1)

        assay_type_id = get_or_insert_assay_type(self.db_path, assay_type_name)
        self.assertEqual(assay_type_id, 1)

        assay_type_name = "MSD"
        assay_type_id = get_or_insert_assay_type(self.db_path, assay_type_name)
        self.assertEqual(assay_type_id, 2)

        assay_type_id = get_or_insert_assay_type(self.db_path, assay_type_name)
        self.assertEqual(assay_type_id, 2)

    def test_get_or_insert_assay(self):
        create_db(self.db_path)

        assay_name, species, assay_type = ["ELISA B2M", "Human", "ELISA"]
        assay_id = get_or_insert_assay(self.db_path, assay_name, species, assay_type)
        self.assertEqual(assay_id, 1)

        assay_id = get_or_insert_assay(self.db_path, assay_name, species, assay_type)
        self.assertEqual(assay_id, 1)

        assay_name, species, assay_type = ["Dupli-R-PLEX TNF-Rs (TNF-RI and TNF-RII)", "Human", "MSD"]
        assay_id = get_or_insert_assay(self.db_path, assay_name, species, assay_type)
        self.assertEqual(assay_id, 2)

        assay_id = get_or_insert_assay(self.db_path, assay_name, species, assay_type)
        self.assertEqual(assay_id, 2)

    def test_add_assay_from_file(self):
        create_db(self.db_path)

        add_assay_from_file(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assay;")
        res = cursor.fetchall()
        conn.close()

        self.assertEqual(len(res), 26)
        self.assertTupleEqual(res[0], (1, 'Dupli-R-PLEX TNF-Rs (TNF-RI and TNF-RII)', 1, 1))
        self.assertTupleEqual(res[1], (2, 'R-PLEX BAFF-R', 1, 1))
        self.assertTupleEqual(res[23], (24, 'ELISA Zonulin', 1, 2))
        self.assertTupleEqual(res[24], (25, 'V-PLEX Proinfammatory P1 Mouse', 2, 1))

    def test_get_or_insert_project_assay(self):
        create_db(self.db_path)

        project_name, assay_name = ["CE-PSY (IF)", "Dupli-R-PLEX TNF-Rs (TNF-RI and TNF-RII)"]
        project_assay_id = get_or_insert_project_assay(self.db_path, project_name, assay_name) 
        self.assertEqual(project_assay_id, 1)

        project_assay_id = get_or_insert_project_assay(self.db_path, project_name, assay_name) 
        self.assertEqual(project_assay_id, 1)