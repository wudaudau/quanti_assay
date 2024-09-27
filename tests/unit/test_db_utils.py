# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.db_utils import * # The code to test
import unittest # The test framework

import os
import tempfile



class TestDBUtils(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for the SQLite database
        self.db_file = tempfile.NamedTemporaryFile(delete=False) # TODO: make it work. It should be a better way to do this.
        self.db_path = "data/database/quanti.sqlite"

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
        self.assertEqual(table_names[0][0], "assay")

        conn.close()
        

    def test_get_table_names(self):
        table_names = get_table_names(self.db_path)
        self.assertEqual(len(table_names), 4)
        self.assertEqual(table_names[0], "assay")
