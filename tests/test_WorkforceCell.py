# -*- coding: utf-8 -*-
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from context import bevcost
import bevcost.TCOmodel as tco


class TestWorkforceCell(unittest.TestCase):

    def assertSeriesEqual(self, df1, df2, msg):
        try:
            assert_series_equal(df1, df2)
        except AssertionError as e:
            raise self.failureException(msg) from e

    @classmethod
    def setUpClass(cls):
        # print("\nsetUpClass method")
        pass

    def setUp(self):
        # print("\nRunning setUp method")
        self.addTypeEqualityFunc(pd.Series, self.assertSeriesEqual)

        opex_dates = {'start date': '2022-01-01',
                      'end date': '2022-02-01'}

        data = {"role": "underground miner",
                "location": "extraction",
                "personnel": {"date": [2022],
                              "workforce size": [10]}}

        business_params = {"labour rates": {"underground miner": 120000.0,
                                            "frequency": "annual"}}

        self.workforce_1 = tco.WorkforceCell(data,
                                             business_params,
                                             opex_dates=opex_dates)

    def tearDown(self):
        # print("\nRunning tearDown method")
        pass

    def test_labour_costs_analysis(self):
        print("\nRunning test_labour_costs_analysis")

        labour_costs = self.workforce_1.labour_costs_analysis()
        test_series = pd.Series(data=[120000/12*10,
                                      120000/12*10],
                                name="labour")
        self.assertEqual(labour_costs["labour"],
                         test_series)

    def test_opex_analysis(self):
        print("\nRunning test_opex_analysis")

        self.workforce_1.opex_analysis()

        self.assertEqual(self.workforce_1.labour_costs["labour"],
                         pd.Series(data=[120000/12*10,
                                         120000/12*10],
                                   name="labour"))

    def test_execute_analysis(self):
        print("\nRunning test_execute_analysis")

        self.workforce_1.execute_analysis()

        self.assertEqual(self.workforce_1.labour_costs["labour"],
                         pd.Series(data=[120000/12*10,
                                         120000/12*10],
                                   name="labour"))

    @classmethod
    def tearDownClass(cls):
        # print("\ntearDownClass method")
        pass

if __name__ == '__main__':
    unittest.main()
