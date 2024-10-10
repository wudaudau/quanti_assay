# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.app import * # The code to test
import unittest # The test framework

from unittest.mock import patch
from io import StringIO

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