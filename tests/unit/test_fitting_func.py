# https://code.visualstudio.com/docs/python/testing#_run-tests
from src.processor.fitting_func import * # The code to test
import unittest # The test framework

class TestFittingFunc(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_arrange_sd_points_in_order(self):
        sd_points = [[1, 2], [3, 4], [2, 3]]
        expected = [[1, 2], [2, 3], [3, 4]]
        actual = arrange_sd_points_in_order(sd_points)
        self.assertEqual(expected, actual)

        # positive slope
        sd_points = [[5, 5], [1, 1], [4, 4], [3, 3], [2, 2]]
        expected = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
        actual = arrange_sd_points_in_order(sd_points)
        self.assertEqual(expected, actual)

        # negative slope
        sd_points = [[1, 5], [3, 3], [5, 1], [2, 4], [4, 2]]
        expected = [[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]]
        actual = arrange_sd_points_in_order(sd_points)
        self.assertEqual(expected, actual)

    def test_determin_sd_slope(self):
        # positive slope
        sd_points = [[5, 5], [1, 1], [4, 4], [3, 3], [2, 2]]
        expected = "pos"
        actual = determin_sd_slope(sd_points)
        self.assertEqual(expected, actual)

        # negative slope
        sd_points = [[1, 5], [3, 3], [5, 1], [2, 4], [4, 2]]
        expected = "neg"
        actual = determin_sd_slope(sd_points)
        self.assertEqual(expected, actual)

        # zero slope (raise ValueError)
        with self.assertRaises(ValueError) as msg:
            sd_points = [[1, 1], [1, 1], [1, 1]]
            determin_sd_slope(sd_points)
            self.assertEqual("The slope of the standard curve is zero.", str(msg.exception))

    def test_cal_init_paras(self):
        # positive slope
        sd_points = [[5, 5], [1, 1], [4, 4], [3, 3], [2, 2]]
        ini_A, ini_B, ini_C, ini_D = cal_init_paras(sd_points)
        self.assertEqual(ini_A, 0.9)
        self.assertEqual(ini_B, 1)
        self.assertEqual(ini_C, 3)
        self.assertAlmostEqual(ini_D, 5.5, places=1)

        # negative slope
        sd_points = [[1, 5], [3, 3], [5, 1], [2, 4], [4, 2]]
        ini_A, ini_B, ini_C, ini_D = cal_init_paras(sd_points)
        self.assertEqual(ini_A, 0.9)
        self.assertEqual(ini_B, -1)
        self.assertEqual(ini_C, 3)
        self.assertAlmostEqual(ini_D, 5.5, places=1)

        # Use one real data
        sd_points = [[0.49, 100], [1.95, 178.5], [7.81, 517], [31.25, 1851], [125, 7344.5], [500, 29599], [2000, 122887]]
        ini_A, ini_B, ini_C, ini_D = cal_init_paras(sd_points)
        self.assertAlmostEqual(ini_A, 90, places=1)
        self.assertEqual(ini_B, 1)
        self.assertAlmostEqual(ini_C, 31.25, places=2)
        self.assertAlmostEqual(ini_D, 135175.7, places=1)


        # zero slope (raise ValueError)
        with self.assertRaises(ValueError) as msg:
            sd_points = [[1, 1], [1, 1], [1, 1]]
            ini_A, ini_B, ini_C, ini_D = cal_init_paras(sd_points)
            self.assertEqual("The slope of the standard curve is zero.", str(msg.exception))

    def test_cal_fitting_paras(self):
        # # positive slope
        # sd_points = [[5, 5], [1, 1], [4, 4], [3, 3], [2, 2]]
        # init_paras = cal_init_paras(sd_points)
        # A, B, C, D = cal_fitting_paras(sd_points, init_paras)
        # # use result from MyCurveFit
        # self.assertAlmostEqual(A, 0.000006761015) # 0.000798071973552989
        # self.assertAlmostEqual(B, 1.000007) # 1.0007808836746175
        # self.assertAlmostEqual(C, 746611.1) # 6286.606306869342
        # self.assertAlmostEqual(D, 746673.8) # 6325.653120389399

        # Use one real data
        sd_points = [[0.49, 100], [1.95, 178.5], [7.81, 517], [31.25, 1851], [125, 7344.5], [500, 29599], [2000, 122887]]
        init_paras = cal_init_paras(sd_points)
        A, B, C, D = cal_fitting_paras(sd_points, init_paras)
        # results from our report
        self.assertAlmostEqual(A, 73.6588, places=4)
        self.assertAlmostEqual(B, 1.0161, places=4)
        self.assertAlmostEqual(C, 937268.2576, places=4)
        self.assertAlmostEqual(D, 63123379.7457, places=4)
        