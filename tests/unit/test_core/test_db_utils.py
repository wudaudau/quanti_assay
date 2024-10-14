# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.core.db_utils import * # The code to test
import unittest # The test framework

import os
import tempfile



class TestDBUtils(unittest.TestCase):
    
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

    def test_create_db(self):
        create_db(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()

        self.assertEqual(len(table_names), 15)
        self.assertEqual(table_names[0][0], "species")
        self.assertEqual(table_names[1][0], "manufacture")
        self.assertEqual(table_names[5][0], "item_lot")
        self.assertEqual(table_names[7][0], "project")
        self.assertEqual(table_names[12][0], "analyte")
        self.assertEqual(table_names[14][0], "assays_analytes")


        conn.close()
        

    def test_get_table_names(self):
        create_db(self.db_path)

        table_names = get_table_names(self.db_path)
        self.assertEqual(len(table_names), 15)
        self.assertEqual(table_names[0], "species")
        self.assertListEqual(table_names, ["species",
                                           "manufacture", "storage", "kit_item", "kits_kit_items",
                                           "item_lot", "sd_initial_conc",
                                           "project", "assay_type", "assay", "sample_type", "project_assay",
                                           "analyte", "analyte_mapping",
                                           "assays_analytes",
                                           ])

    def test_check_exists(self):
        create_db(self.db_path)

        ######
        # A simple table: manufacture
        ######
        manufacture_name = "MSD"

        # check if the manufacture exists
        res = check_exists(self.db_path, "manufacture", {"name": manufacture_name})
        self.assertIsNone(res)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # add a manufacture
        cursor.execute("INSERT INTO manufacture (name) VALUES (?);", (manufacture_name,))
        conn.commit()

        # check if the manufacture exists
        res = check_exists(self.db_path, "manufacture", {"name": manufacture_name})
        self.assertTupleEqual(res, (1,))

        ######
        # A simple table: storage
        ######
        storage_name = "RT"

        # check if the storage exists
        res = check_exists(self.db_path, "storage", {"name": storage_name})
        self.assertIsNone(res)

        # add a storage
        cursor.execute("INSERT INTO storage (name) VALUES (?);", (storage_name,))
        conn.commit()

        # check if the storage exists
        res = check_exists(self.db_path, "storage", {"name": storage_name})
        self.assertTupleEqual(res, (1,))

        ######
        # A table with a foreign key: kit_item
        ######
        kit_cat_number = "R50AA-4" # "Diluent 100"

        # check if the kit_item exists
        res = check_exists(self.db_path, "kit_item", {"kit_cat_number": kit_cat_number})
        self.assertIsNone(res)

        # add a kit_item
        cursor.execute("INSERT INTO kit_item (kit_cat_number, name, manufacture_id, storage_id) VALUES (?,?,?,?);", 
                       (kit_cat_number, "Diluent 100", 1, 1))
        conn.commit()

        # check if the kit_item exists
        res = check_exists(self.db_path, "kit_item", {"kit_cat_number": kit_cat_number})
        self.assertTupleEqual(res, (1,))

        ######
        # A junction table: assays_analytes
        ######
        assay_id, analyte_id, spot, opt_analyte_name = [1, 1, 1, "B2M__ELISA"]
        res = check_exists(self.db_path, "assays_analytes", {"assay_id": assay_id, "analyte_id": analyte_id, "spot": spot})
        self.assertIsNone(res)

        cursor.execute("INSERT INTO assays_analytes (assay_id, analyte_id, spot, opt_analyte_name) VALUES (?,?,?,?);", 
                       (assay_id, analyte_id, spot,opt_analyte_name))
        conn.commit()

        res = check_exists(self.db_path, "assays_analytes", {"assay_id": assay_id, "analyte_id": analyte_id, "spot": spot})
        self.assertTupleEqual(res, (1,))



        conn.close()
        
