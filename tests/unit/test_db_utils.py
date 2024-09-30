# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.db_utils import * # The code to test
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

        self.assertEqual(len(table_names), 6)
        self.assertEqual(table_names[0][0], "manufacture")
        self.assertEqual(table_names[1][0], "storage")
        self.assertEqual(table_names[2][0], "kit_item")
        self.assertEqual(table_names[3][0], "kits_kit_items")
        self.assertEqual(table_names[4][0], "analyte")
        self.assertEqual(table_names[5][0], "analyte_mapping")


        conn.close()
        

    def test_get_table_names(self):
        create_db(self.db_path)

        table_names = get_table_names(self.db_path)
        self.assertEqual(len(table_names), 6)
        self.assertEqual(table_names[0], "manufacture")
        self.assertListEqual(table_names, ["manufacture", "storage", "kit_item", "kits_kit_items",
                                           "analyte", "analyte_mapping"])

    def test_check_exists(self):
        create_db(self.db_path)

        ######
        # A simple table: manufacture
        ######
        manufacture_name = "MSD"

        # check if the manufacture exists
        res = check_exists(self.db_path, "manufacture", "name", manufacture_name)
        self.assertIsNone(res)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # add a manufacture
        cursor.execute("INSERT INTO manufacture (name) VALUES (?);", (manufacture_name,))
        conn.commit()

        # check if the manufacture exists
        res = check_exists(self.db_path, "manufacture", "name", manufacture_name)
        self.assertTupleEqual(res, (1,))

        ######
        # A simple table: storage
        ######
        storage_name = "RT"

        # check if the storage exists
        res = check_exists(self.db_path, "storage", "name", storage_name)
        self.assertIsNone(res)

        # add a storage
        cursor.execute("INSERT INTO storage (name) VALUES (?);", (storage_name,))
        conn.commit()

        # check if the storage exists
        res = check_exists(self.db_path, "storage", "name", storage_name)
        self.assertTupleEqual(res, (1,))

        ######
        # A table with a foreign key: kit_item
        ######
        kit_cat_number = "R50AA-4" # "Diluent 100"

        # check if the kit_item exists
        res = check_exists(self.db_path, "kit_item", "kit_cat_number", kit_cat_number)
        self.assertIsNone(res)

        # add a kit_item
        cursor.execute("INSERT INTO kit_item (kit_cat_number, name, manufacture_id, storage_id) VALUES (?,?,?,?);", 
                       (kit_cat_number, "Diluent 100", 1, 1))
        conn.commit()

        # check if the kit_item exists
        res = check_exists(self.db_path, "kit_item", "kit_cat_number", kit_cat_number)
        self.assertTupleEqual(res, (1,))

        ######
        # A junction table: kits_kit_items
        ######
        # TODO: add a test for the junction table


        conn.close()
        


    def test_get_or_insert_manufacture(self):
        # TODO: the description part is not implemented yet
        create_db(self.db_path)

        manufacture_name = "MSD"
        manufacture_id = get_or_insert_manufacture(self.db_path, manufacture_name)
        self.assertEqual(manufacture_id, 1)

        manufacture_id = get_or_insert_manufacture(self.db_path, manufacture_name)
        self.assertEqual(manufacture_id, 1)

        manufacture_name = "Biovender"
        manufacture_id = get_or_insert_manufacture(self.db_path, manufacture_name)
        self.assertEqual(manufacture_id, 2)

        manufacture_id = get_or_insert_manufacture(self.db_path, manufacture_name)
        self.assertEqual(manufacture_id, 2)


    def test_get_or_insert_storage(self):
        # TODO: the description part is not implemented yet
        create_db(self.db_path)

        storage_name = "RT"
        storage_id = get_or_insert_storage(self.db_path, storage_name)
        self.assertEqual(storage_id, 1)

        storage_id = get_or_insert_storage(self.db_path, storage_name)
        self.assertEqual(storage_id, 1)

        storage_name = "2-8ºC"
        storage_id = get_or_insert_storage(self.db_path, storage_name)
        self.assertEqual(storage_id, 2)

        storage_id = get_or_insert_storage(self.db_path, storage_name)
        self.assertEqual(storage_id, 2)

    def test_get_or_insert_kit_item(self):

        create_db(self.db_path)

        kit_cat_number, name, manufacture, storage, description = ["R50AA-4", "Diluent 100", "MSD", "RT", "Diluent for MSD kit"]
        kit_item_id = get_or_insert_kit_item(self.db_path, kit_cat_number, name, manufacture, storage, description)
        self.assertEqual(kit_item_id, 1)

    def test_add_kit_item_from_file(self):

        create_db(self.db_path)

        add_kit_item_from_file(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kit_item;")
        res = cursor.fetchall()
        conn.close()

        self.assertEqual(len(res), 117)
        self.assertTupleEqual(res[0], (1, '-', 'Plate Seals', 1, 1, 'Adhesive seals for sealing plates during incubations.'))
        self.assertTupleEqual(res[1], (2, 'C0047-2', 'Chemokine Panel 1 (human) Calibrator Blend', 1, 2, 'Ten recombinant human proteins in diluent, buffered and lyophilized. Individual analyte concentration is provided in the lot-specific certificate of analysis (COA).'))

    def test_get_or_insert_analyte(self):
        create_db(self.db_path)

        analyte_name = "IL-6"
        analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
        self.assertEqual(analyte_id, 1)

        analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
        self.assertEqual(analyte_id, 1)

        analyte_name = "TNF-α"
        analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
        self.assertEqual(analyte_id, 2)

        analyte_id = get_or_insert_analyte(self.db_path, analyte_name)
        self.assertEqual(analyte_id, 2)