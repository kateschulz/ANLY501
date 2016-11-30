# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:24:37 2016

@author: kateschulz
"""

# Code taken with modification from http://bokeh.pydata.org/en/latest/docs/gallery/chord_chart.html
import pandas as pd
from bokeh.charts import output_file, Chord
from bokeh.io import show

# Import all bikeshare trips 
trips = pd.read_csv("BikeshareAll.csv")

# Eliminate trips with same start and end station
trips = trips[trips["Start station"] != trips["End station"]]

# List of all unique stations in dataset
Station = pd.unique(trips[['Start station', 'End station']].values.ravel())

# Count of trips between each pair of stations
Freq = trips.groupby(["Start station", "End station"]).size().reset_index(name="Frequency")

# Set the stations as nodes and the number of trips as links
nodes_df = pd.DataFrame(Station)
links_df = pd.DataFrame(Freq)

# Left join node and link dataframes  
source_data = links_df.merge(nodes_df, how='left', left_on='Start station', right_index=True)
source_data = source_data.merge(nodes_df, how='left', left_on='End station', right_index = True)

# Find high-traffic stations 
source_data = source_data[source_data["Frequency"] > 3500]

# Define chord chart
StationChord = Chord(source_data, 
                    source = "Start station", 
                    target = "End station", 
                    value = "Frequency")

# Write output file 
output_file('StationChord.html', mode = "inline")

# Show chord chart
show(StationChord)