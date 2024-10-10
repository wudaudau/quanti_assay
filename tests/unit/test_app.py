# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.app import * # The code to test
import unittest # The test framework

from unittest.mock import patch
from io import StringIO

import tempfile
import os


class TestApp(unittest.TestCase):

    # def setUp(self) -> None:
    #     pass

    # def tearDown(self) -> None:
    #     pass

    # def test_run_app(self):
    #     pass

    @patch('src.app.create_db')
    @patch('src.app.add_kit_item_from_file')
    @patch('src.app.add_analyte_mapping_from_file')
    @patch('src.app.add_assay_from_file')
    @patch('src.app.add_assays_analytes_from_file')
    @patch('src.app.add_project_assay_from_file')
    @patch('src.app.ask_assay_name', return_value='mock_assay')
    @patch('sys.stdout', new_callable=StringIO) # to capture the console output
    def test_run_app(self, mock_stdout, mock_ask_assay_name, 
                     mock_add_project_assay_from_file, mock_add_assays_analytes_from_file, 
                     mock_add_assay_from_file, mock_add_analyte_mapping_from_file, 
                     mock_add_kit_item_from_file, mock_create_db):

        # Run the app
        run_app()

        # Test if create_db was called with the correct argument
        mock_create_db.assert_called_once_with('data/database/quanti.sqlite')

        # Test if data addition functions were called correctly
        mock_add_kit_item_from_file.assert_called_once_with('data/database/quanti.sqlite')
        mock_add_analyte_mapping_from_file.assert_called_once_with('data/database/quanti.sqlite')
        mock_add_assay_from_file.assert_called_once_with('data/database/quanti.sqlite')
        mock_add_assays_analytes_from_file.assert_called_once_with('data/database/quanti.sqlite')
        mock_add_project_assay_from_file.assert_called_once_with('data/database/quanti.sqlite')

        # Test if ask_assay_name was called once
        mock_ask_assay_name.assert_called_once()

        # Test the printed output
        output = mock_stdout.getvalue()
        self.assertIn("Hi, it's the Quanti app!", output)
        self.assertIn("Database has been created.\n", output)
        self.assertIn("Adding data to the database...", output)
        self.assertIn("kit_items.csv have been added to the database.", output)
        self.assertIn("analyte_mappings.csv have been added to the database.", output)
        self.assertIn("assay.csv have been added to the database.", output)
        self.assertIn("assays_analytes.csv have been added to the database.", output)
        self.assertIn("project_assay.csv have been added to the database.", output)

    # TODO: Handle exceptions. No exception is raised in the current implementation.
    # @patch('src.app.create_db', side_effect=Exception("Database creation failed"))
    # @patch('builtins.print')
    # def test_run_app_handles_create_db_exception(self, mock_print, mock_create_db):
    #     # Run the function and catch the exception
    #     with self.assertRaises(Exception):
    #         run_app()

    #     # Verify the error message was printed
    #     mock_print.assert_any_call("Database creation failed")




class TestRunAppWithTempDB(unittest.TestCase):

    def setUp(self):
        # TODO: see if this is consistent with the test in test_assay_planning.py
            # Not exactly the same. Try to make them consistent later.
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.test_dir.name, 'test_quanti.sqlite')

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    @patch('builtins.input', side_effect=['1'])  # Mock input to simulate user entering values
    def test_run_app_integration(self, mock_input):
        # Mock the data loading functions or create test CSV files in the temporary directory

        # Call run_app (modify the code to take the database path as a parameter)
        run_app(self.db_path)

        # Verify the database was created and contains expected data
        # For example, check that some tables exist in the database
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if a specific table exists
        cursor.execute("SELECT assay_id FROM project_assay WHERE id=1;")
        value = cursor.fetchone()
        self.assertEqual(value, (11,))

        # TODO: Check other tables and data

        conn.close()