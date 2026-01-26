"""
Example plots using the TCOmodel.spaghetti_line_plots function.

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
# Create the figure and axes
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

## OPEX Plots
opex1 = pd.Series(data=[250.0, 750.0], 
                 name="energy costs")

opex2 = pd.Series(data=[5.0, 50.0], 
                 name="energy costs")

opex3 = pd.Series(data=[100.0, 1000.0], 
                 name="energy costs")

opex4 = pd.Series(data=[750.0, 100.0], 
                 name="energy costs")

df = pd.DataFrame({
   'x': [2022, 2023],
   'Electricity Costs': opex1.values,
   'Power Costs': opex2.values,
   'BAAS Costs': opex3.values,
   'Automation Software Subscription': opex4.values,
})


# Create a color palette
palette = plt.get_cmap('Dark2')

title = 'test'

ax = tco.spaghetti_line_plots(axes, title, df, palette)

# Add figure title
fig.suptitle(
              title,
              fontsize=16,
              fontweight="bold",
              color='black',
              y=0.95
            )

# Adjust the figure layout
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()