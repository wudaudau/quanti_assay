# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.core.core_tables import * # The code to test
import unittest # The test framework

import os
import tempfile

from src.core.db_utils import create_db

class TestCoreTables(unittest.TestCase):
    
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



    
    def test_get_or_insert_species(self):
        create_db(self.db_path)

        species_name = "Human"
        species_id = get_or_insert_species(self.db_path, species_name)
        self.assertEqual(species_id, 1)

        species_id = get_or_insert_species(self.db_path, species_name)
        self.assertEqual(species_id, 1)

        species_name = "Mouse"
        species_id = get_or_insert_species(self.db_path, species_name)
        self.assertEqual(species_id, 2)

        species_id = get_or_insert_species(self.db_path, species_name)
        self.assertEqual(species_id, 2)

    


