# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 19:34:07 2016

@author: kateschulz
"""

# This file used code (with significant modifications) from http://stackoverflow.com/a/37358401
# DARKER COLORS ==> LOWER MEDIAN INCOME

# Import libraries
from bokeh.sampledata import us_states
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import LogColorMapper, ColumnDataSource, HoverTool
from bokeh.palettes import Viridis6 as palette

import pandas as pd

us_states = us_states.data.copy()

# Definition from https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch04s14.html
def sub_dict(somedict, somekeys, default=None):
    return dict([ (k, somedict.get(k, default)) for k in somekeys ])

region = ['DC', 'MD', 'VA']

dc_md_va = sub_dict(us_states, region)

## Separate latitude and longitude points for the borders
##   of the states.
state_xs = [dc_md_va[code]["lons"] for code in dc_md_va]
state_ys = [dc_md_va[code]["lats"] for code in dc_md_va]

# Tools to inspect feature
FigTools = "pan,wheel_zoom,box_zoom,reset,hover,save"

# Init figure
p = figure(
    title= "Plotting Bikeshare Stations With Median Income", tools=FigTools,
    toolbar_location="left", plot_width=1100, plot_height=700)

# Draw state lines
p.patches(state_xs, state_ys, fill_alpha=0.0,
    line_color="#884444", line_width=1.5)

# Import Data
bikeshare_stations = pd.read_csv("BikeshareStations.csv")

# Define palette on log scale
color_mapper = LogColorMapper(palette=palette)

# Extract longitude (as x), latitude (as y), and median income (as medInc)
source = ColumnDataSource(data=dict(
    x = bikeshare_stations.loc[:,'Longitude'].tolist(),
    y = bikeshare_stations.loc[:,'Latitude'].tolist(),
    medInc = bikeshare_stations.loc[:,'MedIncome'].tolist()))

# The scatter markers
p.circle('x', 'y', source=source,
          fill_color={'field': 'medInc', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5, size = 8)

# Hover tools to inspect image         
hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Median Income","$@medInc{0,000}"),
    ("(Long, Lat)", "($x, $y)")]        

# Output to static HTML file
output_file("bikeshare_stations.html")

# Show results
show(p)