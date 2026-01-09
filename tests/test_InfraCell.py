# -*- coding: utf-8 -*-
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from context import bevcost
import bevcost.TCOmodel as tco


class TestInfraCell(unittest.TestCase):
    
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
        
        infra_data = {"infrastructure type": "charging station",
                      "charger-cooler ratio": 1,
                      "cable length": 100.0,
                      "batteries": 2,
                      "evse": {"LH411B - single charger": 1},
                      "construction schedule": [["2022-02-01", 1.0]],
                      "capex schedule": [["2022-02-01", 1.0]],
                      "BaaS subscription": {"frequency": "monthly",
                                            "dates": {"start date": "2022-01-01",
                                                      "end date": "2022-02-01"}}}
        
        facility_params = {"infrastructure type": "charging station",
                           "development rate ($/m)": 200.0,
                           "development cost": 100000.0,
                           "cable pull ($/m)": 100.0}
        
        evse_params = [{"evse type": "charger",
                        "model": "LH411B - single charger",
                        "charge current": 500.0,
                        "cooling cube power": 100.0,
                        "efficiency": 0.9,
                        "power factor": 0.9,
                        "current derating": 0.9,
                        "BaaS charger monthly rate": 10000.0,
                        "unit price": 50000.0}]
        
        self.infra_1 = tco.InfraCell(infra_data, 
                                     facility_params, 
                                     evse_params,
                                     capex_dates=capex_dates, 
                                     opex_dates=opex_dates)
    
    def tearDown(self):
        # print("\nRunning tearDown method")
        pass
    
    def test_charging_station_analysis(self):
        print("\nRunning test_charging_station_analysis")
        
        construction_costs = self.infra_1.charging_station_analysis()
        construction_costs = construction_costs.set_index("date")
        
        test_series = pd.Series(data=[0, 
                                      110000], 
                                index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                               '2022-02-01']), 
                                               name="date"), 
                                name="charging station costs")
        self.assertEqual(construction_costs["charging station costs"], 
                         test_series)
    
    def test_charging_equipment_analysis(self):
        print("\nRunning test_charging_equipment_analysis")
        
        equipment_costs = self.infra_1.charging_equipment_analysis()
        equipment_costs = equipment_costs.set_index("date")
        
        test_series = pd.Series(data=[0, 
                                      50000], 
                                index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                               '2022-02-01']), 
                                               name="date"), 
                                name="Equipment CAPEX")
        self.assertEqual(equipment_costs["Equipment CAPEX"], 
                         test_series)
    
    def test_baas_costs_analysis(self):
        print("\nRunning test_baas_costs_analysis")
        
        baas_costs = self.infra_1.baas_costs_analysis()
        test_series = pd.Series(data=[10000.0, 
                                      10000.0],
                                name="baas costs")
        self.assertEqual(baas_costs["baas costs"], 
                         test_series)
    
    def test_opex_analysis(self):
        print("\nRunning test_opex_analysis")
        
        self.infra_1.opex_analysis()
        
        self.assertEqual(self.infra_1.baas_costs["baas costs"], 
                         pd.Series(data=[10000.0, 
                                         10000.0],
                                   name="baas costs"))
    
    def test_capex_analysis(self):
        print("\nRunning test_capex_analysis")
        
        self.infra_1.capex_analysis()
        
        self.infra_1.equipment_costs = self.infra_1.equipment_costs.set_index("date")
        self.infra_1.construction_costs = self.infra_1.construction_costs.set_index("date")
        
        self.assertEqual(self.infra_1.equipment_costs["Equipment CAPEX"], 
                         pd.Series(data=[0, 
                                         50000], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="Equipment CAPEX"))
        self.assertEqual(self.infra_1.construction_costs["charging station costs"], 
                         pd.Series(data=[0, 
                                         110000], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="charging station costs"))
    
    def test_execute_analysis(self):
        print("\nRunning test_execute_analysis")
        
        self.infra_1.execute_analysis()
        
        self.infra_1.baas_costs = self.infra_1.baas_costs.set_index("date")
        self.infra_1.equipment_costs = self.infra_1.equipment_costs.set_index("date")
        self.infra_1.construction_costs = self.infra_1.construction_costs.set_index("date")
        
        self.assertEqual(self.infra_1.baas_costs["baas costs"], 
                         pd.Series(data=[10000.0, 
                                         10000.0], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="baas costs"))
        self.assertEqual(self.infra_1.equipment_costs["Equipment CAPEX"], 
                         pd.Series(data=[0, 
                                         50000], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="Equipment CAPEX"))
        self.assertEqual(self.infra_1.construction_costs["charging station costs"], 
                         pd.Series(data=[0, 
                                         110000], 
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"), 
                                   name="charging station costs"))
    
    @classmethod
    def tearDownClass(cls):
        # print("\ntearDownClass method")
        pass

if __name__ == '__main__':
    unittest.main()
    