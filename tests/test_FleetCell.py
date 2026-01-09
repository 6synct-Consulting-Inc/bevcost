# -*- coding: utf-8 -*-
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from context import bevcost
import bevcost.TCOmodel as tco


class TestFleetCell(unittest.TestCase):
    
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
        
        fleet_op_hours = pd.DataFrame({'date': ['2022-01-01', 
                                                '2022-02-01'],
                                       'LHD-1': [100, 
                                                 100]})
        
        production_sched = pd.DataFrame({'date': ['2022-01-01', 
                                                  '2022-02-01'],
                                         'tonnes/month': [100, 
                                                          100]})
        
        business_params = {'energy costs': {'cost per kWh': 0.05,
                                            'cost per kVA': 10.0},
                           'emissions factors': {'grid CO2e emissions': 10.0},
                           'subsidies': {'fuel rebate': 150}}
        
        fleet_params = {'vehicles': 1,
                        'fleet purchase schedule': [['2022-01-01', 0.20], 
                                                    ['2022-02-01', 0.80]],
                        'subsidies': [['2022-02-01', 0.1]]}
        
        vehicles_params_1 = {'energy consumption': 50,
                             'charging power': 200,
                             'evse model': 'single charger',
                             'BaaS monthly rate': 1000,
                             'BaaS charger monthly rate': 10000,
                             'unit price': 500000,
                             'maintenance costs': {"Machine Hours": [250, 
                                                                     500, 
                                                                     750, 
                                                                     1000],
                                                   "Major Components": [10000, 
                                                                        20000, 
                                                                        25000, 
                                                                        30000]}}
        
        evse_params = {"model": "single charger",
                       "cooling cube power": 50,
                       "efficiency": 0.9,
                       "power factor": 0.9,
                       "BaaS charger monthly rate": 10000}
        
        self.fleet_1 = tco.FleetCell(fleet_params, 
                                     vehicles_params_1,
                                     evse_params,
                                     business_params, 
                                     fleet_op_hours, 
                                     capex_dates=capex_dates,
                                     opex_dates=opex_dates,
                                     production_sched=production_sched,
                                     location=None)
    
    def tearDown(self):
        # print("\nRunning tearDown method")
        pass
    
    def test_energy_consumption_analysis(self):
        print("\nRunning test_energy_consumption_analysis")
        
        fleet1_energy_consumed = self.fleet_1.energy_consumption_analysis()
        self.assertEqual(fleet1_energy_consumed["energy consumption"], 
                         pd.Series(data=[5000, 5000], 
                                   name="energy consumption"))
        
    def test_energy_cost_analysis(self):
        print("\nRunning test_energy_cost_analysis")
        
        self.fleet_1.energy_consumed = pd.DataFrame({'date': ['2022-01-01', '2022-02-01'],
                                                     'energy consumption': [5000, 5000]})
        
        fleet1_energy_costs = self.fleet_1.energy_cost_analysis()
        self.assertEqual(fleet1_energy_costs["energy costs"], 
                         pd.Series(data=[250.0, 250.0], 
                                   name="energy costs"))
        
    def test_peak_power(self):
        print("\nRunning test_peak_power")
        
        evse_name = self.fleet_1.vehicles_params["evse model"]
        evse_num = self.fleet_1.vehicles_required.iat[0,0]
        
        peak_power = self.fleet_1.peak_power(evse_name, evse_num)
        self.assertEqual(peak_power, 
                         100.0/0.9/0.9)
        
    def test_power_consumption_analysis(self):
        print("\nRunning test_power_consumption_analysis")
        
        fleet1_power_consumed = self.fleet_1.power_consumption_analysis()
        self.assertEqual(fleet1_power_consumed["power consumption"], 
                         pd.Series(data=[100.0/0.9/0.9, 100.0/0.9/0.9], 
                                   name="power consumption"))
        
    def test_power_cost_analysis(self):
        print("\nRunning test_power_cost_analysis")
        
        self.fleet_1.power_consumed = pd.DataFrame({'date': ['2022-01-01', '2022-02-01'],
                                                     'power consumption': [100, 100]})
        
        fleet1_power_costs = self.fleet_1.power_cost_analysis()
        self.assertEqual(fleet1_power_costs["power costs"], 
                         pd.Series(data=[1000.0, 1000.0], 
                                   name="power costs"))
        
    def test_GHG_emissions_analysis(self):
        print("\nRunning test_GHG_emissions_analysis")
        
        self.fleet_1.energy_consumed = pd.DataFrame({'date': ['2022-01-01', '2022-02-01'],
                                                     'energy consumption': [5000, 5000]})
        
        fleet1_GHG_emissions = self.fleet_1.GHG_emissions_analysis()
        self.assertEqual(fleet1_GHG_emissions["emissions"], 
                         pd.Series(data=[50.0, 50.0], 
                                   name="emissions"))
        
    def test_baas_costs_analysis(self):
        print("\nRunning test_baas_costs_analysis")
        
        fleet1_baas_costs = self.fleet_1.baas_costs_analysis()
        self.assertEqual(fleet1_baas_costs["baas costs"], 
                         pd.Series(data=[11000, 11000], 
                                   name="baas costs"))
    
    def test_maint_interval_costs(self):
        print("\nRunning test_maint_interval_costs")
        
        cost_intervals = pd.DataFrame(self.fleet_1.vehicles_params['maintenance costs'])
        op_hours = self.fleet_1.fleet_op_hours['LHD-1'].iat[-1]
        cumul_op_hours = self.fleet_1.fleet_op_hours['LHD-1'].cumsum().iat[-1]
        
        maintenance_costs = self.fleet_1.maint_interval_costs(cumul_op_hours, 
                                                              op_hours, 
                                                              cost_intervals)
        self.assertEqual(maintenance_costs, 
                         4000.0)
    
    def test_maintenance_costs_analysis(self):
        print("\nRunning test_maintenance_costs_analysis")
        
        fleet_1_bev_maint_costs, fleet_1_maintenance_costs = self.fleet_1.maintenance_costs_analysis()
        self.assertEqual(fleet_1_bev_maint_costs["LHD-1"], 
                         pd.Series(data=[4000, 4000], 
                                   name="LHD-1"))
        self.assertEqual(fleet_1_maintenance_costs["maintenance costs"], 
                         pd.Series(data=[4000, 4000], 
                                   name="maintenance costs"))
    
    def test_opex_subsidies_analysis(self):
        print("\nRunning test_opex_subsidies_analysis")
        
        self.fleet_1.energy_consumed = pd.DataFrame({'date': ['2022-01-01', '2022-02-01'],
                                                     'energy consumption': [5000, 5000]})
        
        fleet_1_opex_subsidies = self.fleet_1.opex_subsidies_analysis()
        fleet_1_opex_subsidies = fleet_1_opex_subsidies.set_index("date")
        
        self.assertEqual(fleet_1_opex_subsidies["opex subsidies"], 
                         pd.Series(data=[-750.0, 
                                         -750.0],
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"),
                                   name="opex subsidies"))
    
    def test_fleet_purchase_analysis(self):
        print("\nRunning test_fleet_purchase_analysis")
        
        fleet_1_fleet_costs = self.fleet_1.fleet_purchase_analysis()
        self.assertEqual(fleet_1_fleet_costs["fleet capex"], 
                         pd.Series(data=[100000, 400000], 
                                   name="fleet capex"))
    
    def test_capex_subsidies_analysis(self):
        print("\nRunning test_capex_subsidies_analysis")
        
        fleet_1_capex_subsidies = self.fleet_1.capex_subsidies_analysis()
        fleet_1_capex_subsidies = fleet_1_capex_subsidies.set_index("date")
        
        self.assertEqual(fleet_1_capex_subsidies["capex subsidies"], 
                         pd.Series(data=[0, 
                                         -50000],
                                   index=pd.Index(pd.to_datetime(['2022-01-01', 
                                                                  '2022-02-01']), 
                                                  name="date"),
                                   name="capex subsidies"))
    
    def test_opex_analysis(self):
        print("\nRunning test_opex_analysis")
        
        self.fleet_1.opex_analysis()
        
        self.assertEqual(self.fleet_1.energy_consumed["energy consumption"], 
                         pd.Series(data=[5000, 5000], 
                                   name="energy consumption"))
        self.assertEqual(self.fleet_1.energy_costs["energy costs"], 
                         pd.Series(data=[250.0, 250.0], 
                                   name="energy costs"))
        self.assertEqual(self.fleet_1.GHG_emissions["emissions"], 
                         pd.Series(data=[50.0, 50.0], 
                                   name="emissions"))
        self.assertEqual(self.fleet_1.baas_costs["baas costs"], 
                         pd.Series(data=[11000, 11000], 
                                   name="baas costs"))
        self.assertEqual(self.fleet_1.maintenance_costs["maintenance costs"], 
                         pd.Series(data=[4000, 4000], 
                                   name="maintenance costs"))
        self.assertEqual(self.fleet_1.opex_subsidies["opex subsidies"], 
                         pd.Series(data=[-750.0, -750.0], 
                                   name="opex subsidies"))
    
    def test_capex_analysis(self):
        print("\nRunning test_capex_analysis")
        
        self.fleet_1.capex_analysis()
        
        self.assertEqual(self.fleet_1.fleet_costs["fleet capex"], 
                         pd.Series(data=[100000, 400000], 
                                   name="fleet capex"))
        self.assertEqual(self.fleet_1.capex_subsidies["capex subsidies"], 
                         pd.Series(data=[0, -50000], 
                                   name="capex subsidies"))
        
    def test_execute_analysis(self):
        print("\nRunning test_execute_analysis")
        
        self.fleet_1.execute_analysis()
        
        self.assertEqual(self.fleet_1.energy_consumed["energy consumption"], 
                         pd.Series(data=[5000, 5000], 
                                   name="energy consumption"))
        self.assertEqual(self.fleet_1.energy_costs["energy costs"], 
                         pd.Series(data=[250.0, 250.0], 
                                   name="energy costs"))
        self.assertEqual(self.fleet_1.GHG_emissions["emissions"], 
                         pd.Series(data=[50.0, 50.0], 
                                   name="emissions"))
        self.assertEqual(self.fleet_1.baas_costs["baas costs"], 
                         pd.Series(data=[11000, 11000], 
                                   name="baas costs"))
        self.assertEqual(self.fleet_1.maintenance_costs["maintenance costs"], 
                         pd.Series(data=[4000, 4000], 
                                   name="maintenance costs"))
        self.assertEqual(self.fleet_1.opex_subsidies["opex subsidies"], 
                         pd.Series(data=[-750.0, -750.0], 
                                   name="opex subsidies"))
        self.assertEqual(self.fleet_1.fleet_costs["fleet capex"], 
                         pd.Series(data=[100000, 400000], 
                                   name="fleet capex"))
        self.assertEqual(self.fleet_1.capex_subsidies["capex subsidies"], 
                         pd.Series(data=[0, -50000], 
                                   name="capex subsidies"))
        
    @classmethod
    def tearDownClass(cls):
        # print("\ntearDownClass method")
        pass

if __name__ == '__main__':
    unittest.main()
    