"""
Example plots using the TCOmodel.stacked_bar_chart function.

This script contains four examples showing how the stacked_bar_chart function
works. The examples demonstrate how TCO costs can be compared between different
categories of equipment and how they can be compared over time for one type/piece
of equipment. 

Two examples use simple datasets (lists of cost data) while two use a more
advanced plotting method utilizing Pandas Series objects, like those created 
by the core TCOmodel classes.
"""
# Import libraries and packages
import matplotlib.pyplot as plt
import pandas as pd
import bevcost.TCOmodel as tco

## Example 1: Simple equipment comparison
# Create the figure
fig, ax = plt.subplots()

# Sample dataset containing costs for categories of equipment
# Each sub-list in the 'data' list object relates to one cost component
data = {'x': ["BEV LHD", "BEV Truck", "BEV Jumbo", "BEV LDV", "BEV Utility"],
        'cost labels': ['Vehicle Purchase', 'Energy', 'Maintenance', 'Chargers'],
        'data': [[0.25, 0.05, 0.01, 0.08, 0.1],
                 [0.5, 0.15, 0.1, 0.16, 0.05],
                 [0.08, 0.22, 0.35, 0.18, 0.21],
                 [0.41, 0.0, 0.11, 0.12, 0.17]]}

# Provide label details (label name and formatting)
x_label = "Mining Equipment"
label_formats={'x': '${x:,.2f}', 'y': None}

# Create the stacked bar chart
ax = tco.stacked_bar_chart(ax,
                           data,
                           x_label=x_label)

# Add a title
ax.set_title("Equipment TCO Comparison", fontweight="bold")

plt.show()


## Example 2: Simple annual comparison
# Create the figure
fig, ax = plt.subplots()

# Sample dataset containing annual costs
# Each sub-list in the 'data' list object relates to one cost component
data = {'x': [2022, 2023, 2024, 2025, 2026],
        'cost labels': ['BaaS', 'Energy', 'Power', 'Maintenance'],
        'data': [[0.16, 0.51, 0.34, 0.24, 0.18],
                 [0.25, 0.08, 0.15, 0.60, 0.16],
                 [0.14, 0.02, 0.05, 0.26, 0.71],
                 [0.33, 0.44, 0.0, 0.10, 0.06]]}

# Provide label details (label name and formatting)
x_label = None
label_formats={'x': '${x:,.2f}', 'y': None}

# Create the stacked bar chart
ax = tco.stacked_bar_chart(ax,
                           data,
                           x_label=x_label)

# Add a title
ax.set_title("Annual LHD TCO", fontweight="bold")

plt.show()


## Example 3: Advanced annual comparison
# Create the figure
fig, ax = plt.subplots(figsize=(3,5))

# Advanced dataset containing annual costs using Pandas Series objects
# Each Pandas Series object relates to one cost component, Series must have a 
# name as this is where the 'cost labels' are defined
data = {'x': [f"{_.month}/{_.year}" for _ in pd.to_datetime(["2026/01/01", "2027/01/01"])],
        'cost labels': None,
        'data':[pd.Series(data=[5000, 5000],
                          name="energy consumption"),
                pd.Series(data=[3000, 1000],
                          name="power consumption"),
                pd.Series(data=[500, 1500],
                          name="BaaS")]}

# Provide label details (label name and formatting)
x_label = 'Time'
label_formats = {'x': '${x:,.0f}',
                 'y': None}

# Create the stacked bar chart
ax = tco.stacked_bar_chart(ax,
                           data,
                           x_label=x_label,
                           label_formats=label_formats)

# Add a title
ax.set_title("Annual LHD TCO", fontweight="bold")

plt.show()


## Example 4: Advanced equipment comparison
# Create the figure
fig, ax = plt.subplots(figsize=(5,5))

# Advanced dataset containing equipment costs using Pandas Series objects
# Each Pandas Series object relates to one cost component, Series must have a 
# name as this is where the 'cost labels' are defined
data = {'x': ["BEV Trucks", "BEV LHDs", "BEV Jumbos"],
        'cost labels': None,
        'data': [pd.Series(data=[6500, 5000, 2500],
                           name="Energy"),
                 pd.Series(data=[3000, 1000, 600],
                           name="Power"),
                 pd.Series(data=[500, 1500, 300],
                           name="BaaS")]}

# Provide label details (label name and formatting)
x_label = "Mining Equipment"
label_formats={'x': '${x:,.0f}', 'y': None}

# Create the stacked bar chart
ax = tco.stacked_bar_chart(ax,
                            data,
                            x_label=x_label,
                            label_formats=label_formats)

# Add a title
ax.set_title("Equipment TCO Comparison", fontweight="bold")

plt.show()



# data = {'x': pd.to_datetime(["2026/01/01", "2027/01/01"]),
#         'cost labels': None,
#         'data':[pd.Series(data=[5000, 5000],
#                           index=pd.to_datetime(["2026/01/01", "2027/01/01"], format="%Y/%m/%d"),
#                           name="energy consumption"),
#                 pd.Series(data=[3000, 1000],
#                           index=pd.to_datetime(["2026/01/01", "2027/01/01"], format="%Y/%m/%d"),
#                           name="power consumption"),
#                 pd.Series(data=[500, 1500],
#                           index=pd.to_datetime(["2026/01/01", "2027/01/01"], format="%Y/%m/%d"),
#                           name="BaaS")]}
