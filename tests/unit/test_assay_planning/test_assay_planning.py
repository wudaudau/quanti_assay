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

        self.assertEqual(len(res), 14)
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

    def test_get_or_insert_sample_type(self):
        create_db(self.db_path)

        sample_type_name = "Serum"
        sample_type_id = get_or_insert_sample_type(self.db_path, sample_type_name)
        self.assertEqual(sample_type_id, 1)

        sample_type_id = get_or_insert_sample_type(self.db_path, sample_type_name)
        self.assertEqual(sample_type_id, 1)

        sample_type_name = "Plasma (EDTA)"
        sample_type_id = get_or_insert_sample_type(self.db_path, sample_type_name)
        self.assertEqual(sample_type_id, 2)

        sample_type_id = get_or_insert_sample_type(self.db_path, sample_type_name)
        self.assertEqual(sample_type_id, 2)

    # def test_get_or_insert_project_assay(self):
    #     create_db(self.db_path)

    #     project_name, assay_name = ["CE-PSY (IF)", "Dupli-R-PLEX TNF-Rs (TNF-RI and TNF-RII)"]
    #     project_assay_id = get_or_insert_project_assay(self.db_path, project_name, assay_name) 
    #     self.assertEqual(project_assay_id, 1)

    #     project_assay_id = get_or_insert_project_assay(self.db_path, project_name, assay_name) 
    #     self.assertEqual(project_assay_id, 1)

    # def test_add_project_assay_from_file(self):
    #     create_db(self.db_path)

    #     add_project_assay_from_file(self.db_path)

    #     conn = sqlite3.connect(self.db_path)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM project_assay;")
    #     res = cursor.fetchall()
    #     conn.close()

    #     self.assertEqual(len(res), 35) # TODO: not 36???
    #     self.assertTupleEqual(res[0], (1, 1, 1))
    #     self.assertTupleEqual(res[1], (2, 1, 2))
    #     self.assertTupleEqual(res[6], (7, 1, 7))





    
    # def test_get_or_insert_analyte(self):
    #     create_db(self.db_path)

    #     analyte_name = "IL-6"
    #     analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
    #     self.assertEqual(analyte_id, 1)

    #     analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
    #     self.assertEqual(analyte_id, 1)

    #     analyte_name = "TNF-α"
    #     analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
    #     self.assertEqual(analyte_id, 2)

    #     analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
    #     self.assertEqual(analyte_id, 2)

    # def test_get_or_insert_analyte_mapping(self):
    #     create_db(self.db_path)

    #     analyte_name, std_analyte_name = ["TNF-α", "TNF_alpha"]
    #     analyte_mapping_id = get_or_insert_analyte_mapping(self.db_path, analyte_name, std_analyte_name)
    #     self.assertEqual(analyte_mapping_id, 1)

    #     analyte_mapping_id = get_or_insert_analyte_mapping(self.db_path, analyte_name, std_analyte_name)
    #     self.assertEqual(analyte_mapping_id, 1)

    #     analyte_name, std_analyte_name = ["TNF-a", "TNF_alpha"]
    #     analyte_mapping_id = get_or_insert_analyte_mapping(self.db_path, analyte_name, std_analyte_name)
    #     self.assertEqual(analyte_mapping_id, 2)

    #     analyte_mapping_id = get_or_insert_analyte_mapping(self.db_path, analyte_name, std_analyte_name)
    #     self.assertEqual(analyte_mapping_id, 2)

    #     analyte_name, std_analyte_name = ["TNF-alpha", "TNF_alpha"]
    #     analyte_mapping_id = get_or_insert_analyte_mapping(self.db_path, analyte_name, std_analyte_name)
    #     self.assertEqual(analyte_mapping_id, 3)

    #     analyte_mapping_id = get_or_insert_analyte_mapping(self.db_path, analyte_name, std_analyte_name)
    #     self.assertEqual(analyte_mapping_id, 3)

    # def test_add_analyte_mapping_from_file(self):
    #     create_db(self.db_path)

    #     add_analyte_mapping_from_file(self.db_path)

    #     conn = sqlite3.connect(self.db_path)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM analyte_mapping;")
    #     res = cursor.fetchall()
    #     conn.close()

    #     self.assertEqual(len(res), 72)
    #     self.assertTupleEqual(res[0], (1, 'ApoE', 1))
    #     self.assertTupleEqual(res[20], (21, 'IL-17A', 21))
    #     self.assertTupleEqual(res[21], (22, 'IL-17A Gen. B', 22))




    # def test_get_or_insert_assays_analytes(self):
    #     create_db(self.db_path)

    #     assay_name, analyte_name, spot, opt_analyte_name = ["ELISA B2M", "B2M", 1, "B2M__ELISA"]
    #     assays_analytes_id = get_or_insert_assays_analytes(self.db_path, assay_name, analyte_name, spot, opt_analyte_name)
    #     self.assertEqual(assays_analytes_id, 1)

    #     assays_analytes_id = get_or_insert_assays_analytes(self.db_path, assay_name, analyte_name, spot, opt_analyte_name)
    #     self.assertEqual(assays_analytes_id, 1)

    # def test_add_assays_analytes_from_file(self):
    #     create_db(self.db_path)
    #     # add_assay_from_file(self.db_path)

    #     add_assays_analytes_from_file(self.db_path)

    #     conn = sqlite3.connect(self.db_path)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM assays_analytes;")
    #     res = cursor.fetchall()
    #     conn.close()

    #     self.assertEqual(len(res), 74)
    #     self.assertTupleEqual(res[0], (1, 1, 1, 1, 'GM_CSF__CytoP1'))
    #     self.assertTupleEqual(res[20], (21, 3, 21, 1, 'IP_10__MetaG1'))
    #     self.assertTupleEqual(res[21], (22, 3, 22, 3, 'IL_1RA__MetaG1'))


    #     # TODO: this is the version with add_assay_from_file(self.db_path) after the database is created
    #         # we will see if we need this function or need to update the values after the schema transformation is done
    #     # self.assertTupleEqual(res[0], (1, 11, 1, 1, 'GM_CSF__CytoP1'))
    #     # self.assertTupleEqual(res[20], (21, 8, 21, 1, 'IP_10__MetaG1'))
    #     # self.assertTupleEqual(res[21], (22, 8, 22, 3, 'IL_1RA__MetaG1'))
