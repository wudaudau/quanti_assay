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

        self.assertEqual(len(table_names), 4)
        self.assertEqual(table_names[0][0], "manufacture")

        conn.close()
        

    def test_get_table_names(self):
        create_db(self.db_path)

        table_names = get_table_names(self.db_path)
        self.assertEqual(len(table_names), 4)
        self.assertEqual(table_names[0], "manufacture")

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