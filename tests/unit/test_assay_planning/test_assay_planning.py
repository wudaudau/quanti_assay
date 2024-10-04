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