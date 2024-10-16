# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.kit_order.kit_order import * # The code to test
import unittest # The test framework

import os
import tempfile

from src.core.db_utils import create_db

class TestKitOrder(unittest.TestCase):

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

    def test_get_or_insert_quanti_item_type(self):

        create_db(self.db_path)

        quanti_item_type_name, description = ["Kit", "Assay kit"]
        quanti_item_type_id = get_or_insert_quanti_item_type(self.db_path, quanti_item_type_name, description)
        self.assertEqual(quanti_item_type_id, 1)

        quanti_item_type_id = get_or_insert_quanti_item_type(self.db_path, quanti_item_type_name, description)
        self.assertEqual(quanti_item_type_id, 1)

        quanti_item_type_name, description = ["Item-SD", "Calibrator for the assay kit"]
        quanti_item_type_id = get_or_insert_quanti_item_type(self.db_path, quanti_item_type_name, description)
        self.assertEqual(quanti_item_type_id, 2)

        quanti_item_type_id = get_or_insert_quanti_item_type(self.db_path, quanti_item_type_name, description)
        self.assertEqual(quanti_item_type_id, 2)

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






