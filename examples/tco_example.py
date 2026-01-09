# -*- coding: utf-8 -*-
"""
Basic example
"""
# Import libraries
import pandas as pd
import json
import matplotlib.pyplot as plt
import os
# import TCOmodel as tco
import bevcost.TCOmodel as tco
#from scipy.stats import weibull_min
import numpy as np
import math
import calendar

# from context import bevcost
import bevcost.TCOmodel as tco

"""
Total Cost of Ownership (TCO) analysis
"""
# Set up working directories
wd = os.getcwd()
par_dir = os.path.abspath(os.path.join(wd, os.pardir))
data_dir = os.path.join(par_dir, "examples")
out_dir = os.path.join(par_dir, "examples")


"""
Import TCO analysis data
"""
# Import input data on vehicles, support equipment, infrastructure, etc.
equipment_json_path = os.path.join(data_dir, 'data.json')

with open(equipment_json_path, 'r') as file:
    equipment_data = json.load(file)

infrastructure_data = equipment_data["infrastructure"]
digital_solutions_data = equipment_data["digital solutions"]

# Import TCO anlaysis data
tco_analysis_path = os.path.join(data_dir, 'analysis.json')

with open(tco_analysis_path, 'r') as file:
    analysis_data = json.load(file)

# Import TCO analysis start and end dates
project_name = analysis_data["analysis"]["project name"]
capex_dates = analysis_data["analysis"]["CAPEX"]
opex_dates = analysis_data["analysis"]["OPEX"]

"""
Fleet analysis
"""
# Import business case data
business_params = analysis_data["business"]

# Import vehicle data
LHD_data = equipment_data["vehicles"]
LHD_dict = tco.list_to_dict(LHD_data, "model")

# Import support equipment data
evse_data = equipment_data["support equipment"]
evse_dict = tco.list_to_dict(evse_data, "model")

fleet_stock = []

for fleet_params in analysis_data["fleet"]:
    
    fleet_op_hours = pd.DataFrame(data=fleet_params["fleet operating hours"][1:],
                                  columns=fleet_params["fleet operating hours"][0])
    
    fleet_op_hours["date"] = pd.to_datetime(fleet_op_hours["date"])
    
    vehicles_params = LHD_dict[fleet_params["model"]]
    
    evse_params = evse_dict[vehicles_params["evse model"]]
    
    # Create fleet instance and determine costs
    fleet_1 = tco.FleetCell(fleet_params, 
                            vehicles_params,
                            evse_params,
                            business_params, 
                            fleet_op_hours, 
                            capex_dates=capex_dates,
                            opex_dates=opex_dates,
                            production_sched=None,
                            location=fleet_params["location"])
    
    fleet_1.execute_analysis()
    
    fleet_stock.append(fleet_1)

"""
Infrastructure analysis
""" 
facility_params = infrastructure_data[0]

infra_stock = []

for infra_params in analysis_data["infrastructure"]:
    # Import support equipment data
    evse_params2 = [evse_dict[_] for _ in infra_params["evse"]]
    
    # Create infrastructure instance and determine costs
    infra_1 = tco.InfraCell(infra_params, 
                            facility_params, 
                            evse_params2,
                            capex_dates=capex_dates, 
                            opex_dates=opex_dates,
                            location=infra_params["location"])
    
    infra_1.execute_analysis()
    
    infra_stock.append(infra_1)

"""
Digital solutions analysis
"""
# Import digital solutions data
solutions_params = digital_solutions_data[0]

digital_stock = []

for solutions_data in analysis_data["digital solutions"]:
    # Create digital solutions instance and determine costs
    digital = tco.DigitalSolutionsCell(solutions_data,
                                       solutions_params,
                                       capex_dates=capex_dates, 
                                       opex_dates=opex_dates,
                                       location=solutions_data["location"])
    
    digital.execute_analysis()
    
    digital_stock.append(digital)

"""
Workforce analysis
"""
workforce_pool = []

for workforce_params in analysis_data["workforce"]:
    # Create workforce instance and determine costs
    workforce_1 = tco.WorkforceCell(workforce_params,
                                    business_params,
                                    opex_dates=opex_dates,
                                    location=workforce_params["location"])
    
    workforce_1.execute_analysis()
    
    workforce_pool.append(workforce_1)

"""
Electric mine TCO analysis
"""

(opex_objects, opex_vars), (capex_objects, capex_vars) = tco.annual_cashflow_summary(fleet_objects=fleet_stock, 
                                                                                      infra_objects=infra_stock, 
                                                                                      labour_objects=workforce_pool, 
                                                                                      digital_solution_objects=digital_stock)

# (opex_objects, opex_vars), (capex_objects, capex_vars) = tco.annual_cashflow_summary(fleet_objects=None, 
#                                                                                      infra_objects=None, 
#                                                                                      labour_objects=None, 
#                                                                                      digital_solution_objects=digital_stock)


# Concatenate all opex objects
new_col_names = [list(f"{name} " + costs.keys()) for name, costs in opex_objects.items()]
flattened_col_names = [_ for sublist in new_col_names for _ in sublist]

opex_concat = pd.concat(opex_objects, axis=1)
opex_concat.columns = flattened_col_names
opex_concat["total opex"] = opex_concat.sum(axis=1)

# Concatenate all capex objects
new_col_names = [list(f"{name} " + costs.keys()) for name, costs in capex_objects.items()]
flattened_col_names = [_ for sublist in new_col_names for _ in sublist]

capex_concat = pd.concat(capex_objects, axis=1)
capex_concat.columns = flattened_col_names
capex_concat["total capex"] = capex_concat.sum(axis=1)


# capex, opex, production, consumption, waste = tco.tco_summary([fleet_1], 
#                                                               [infra_1], 
#                                                               [workforce_1],
#                                                               [digital_1],
#                                                               verbose=True)