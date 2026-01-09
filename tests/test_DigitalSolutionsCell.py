# -*- coding: utf-8 -*-
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from context import bevcost
import bevcost.TCOmodel as tco


class TestDigitalSolutionsCell(unittest.TestCase):
    
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
        
        capex_dates = {'start date': '2022-01-01', 
                       'end date': '2022-02-01'}
        
        opex_dates = {'start date': '2022-01-01', 
                      'end date': '2022-02-01'}
        
        data = {"location": "IOC",
                "type": "software",
                "evse": {"workshop charger": 1},
                "capex schedule": [["2022-01-01", 1.0]],
                "opex schedule": [["2022-01-01", 1.0],
                                  ["2022-02-01", 1.0]]}
        
        solutions_params = {"infrastructure type": "software",
                            "solution name": "Fleet Management System",
                            "unit price": 200000,
                            "subscription price": 25000}
        
        self.digital_1 = tco.DigitalSolutionsCell(data,
                                                solutions_params,
                                                capex_dates=capex_dates, 
                                                opex_dates=opex_dates)
    
    def tearDown(self):
        # print("\nRunning tearDown method")
        pass
    
    def test_commission_analysis(self):
        print("\nRunning test_solution_install_analysis")
        
        software_costs = self.digital_1.commission_analysis()
        software_costs = software_costs.set_index("date")
        
        test_series = pd.Series(data=[200000, 
                                      0], 
                                index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                               '2022-02-01']), 
                                               name="date"), 
                                name="Software CAPEX")
        self.assertEqual(software_costs["Software CAPEX"], 
                         test_series)
    
    def test_subscription_analysis(self):
        print("\nRunning test_solution_subscription_analysis")
        
        software_subs = self.digital_1.subscription_analysis()
        software_subs = software_subs.set_index("date")
        
        test_series = pd.Series(data=[25000, 
                                      25000], 
                                index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                               '2022-02-01']), 
                                               name="date"), 
                                name="Software OPEX")
        self.assertEqual(software_subs["Software OPEX"], 
                         test_series)
    
    def test_opex_analysis(self):
        print("\nRunning test_opex_analysis")
        
        self.digital_1.opex_analysis()
        
        software_subs = self.digital_1.software_subs
        software_subs = software_subs.set_index("date")
        
        self.assertEqual(software_subs["Software OPEX"], 
                         pd.Series(data=[25000, 
                                         25000],
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"),
                                   name="Software OPEX"))
    
    def test_capex_analysis(self):
        print("\nRunning test_capex_analysis")
        
        self.digital_1.capex_analysis()
        
        software_costs = self.digital_1.software_costs
        software_costs = software_costs.set_index("date")
        
        self.assertEqual(software_costs["Software CAPEX"], 
                         pd.Series(data=[200000, 
                                         0], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="Software CAPEX"))
    
    def test_execute_analysis(self):
        print("\nRunning test_execute_analysis")
        
        self.digital_1.execute_analysis()
        
        software_subs = self.digital_1.software_subs
        software_subs = software_subs.set_index("date")
        
        software_costs = self.digital_1.software_costs
        software_costs = software_costs.set_index("date")
        
        self.assertEqual(software_subs["Software OPEX"], 
                         pd.Series(data=[25000, 
                                         25000],
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"),
                                   name="Software OPEX"))
        self.assertEqual(software_costs["Software CAPEX"], 
                         pd.Series(data=[200000, 
                                         0], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="Software CAPEX"))
    
    @classmethod
    def tearDownClass(cls):
        # print("\ntearDownClass method")
        pass

if __name__ == '__main__':
    unittest.main()
    