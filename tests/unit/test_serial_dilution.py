# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.processor.serial_dilution import * # The code to test
import unittest # The test framework


class TestSerialDilution(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_cal_sd7_dilution_factor(self):
        sd_vol = 100
        other_vol = 900
        expected = 0.1
        actual = cal_sd7_dilution_factor(sd_vol, other_vol)
        self.assertEqual(expected, actual)

    def test_cal_sd7_conc(self):
        sd_conc = 5000
        sd7_dilution_factor = 0.1
        expected = 500
        actual = cal_sd7_conc(sd_conc, sd7_dilution_factor)
        self.assertEqual(expected, actual)

    def test_cal_sd_serie_conc(self):
        sd7_conc = 2000
        serial_dilution_factor = 4
        expected = [0.49, 1.95, 7.81, 31.25, 125, 500, 2000]
        actual = cal_sd_serie_conc(sd7_conc, serial_dilution_factor)
        self.assertEqual(expected, actual)