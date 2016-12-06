# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:14:28 2016

@author: kateschulz
"""

import pandas as pd

# Import bikeshare and weather data
all_bikeshare_data = pd.read_csv("BikeshareAllDatesSplit.csv")
weather_data = pd.read_csv("WeatherWithFeatures.csv")

# Left join bikeshare and weather data on common fields
complete = pd.merge(all_bikeshare_data, weather_data, how='left', 
                    on=['Month', 'Day of Month'])

# Group trips by each day
groups = pd.DataFrame({'count' : complete.groupby( 
                    [ 'Start date','Member type','Avg Temp'] ).size()}).reset_index()

# Group the casual trips for each day
casTrips = groups[groups["Member type"] == "Casual"] 

# Set up casual trip count for final output
casCount = casTrips.loc[:, ["count"]]
casCount = casCount.reset_index(drop = True)
casCount = casCount.rename(columns={'count': 'Casual Trips'})

# Group the registered trips for each day
regTrips = groups[groups["Member type"] == "Registered"]

# Set up registered trip count for final output
regCount = regTrips.loc[:, ["count"]]
regCount = regCount.reset_index(drop = True)
regCount = regCount.rename(columns={'count': 'Registered Trips'})

# Get all dates in the year
Date = regTrips.loc[:, ["Start date"]]
Date = Date.reset_index(drop = True)

# Get all daily temperatures in the year
Temp = regTrips.loc[:, ['Avg Temp']]
Temp = Temp.reset_index(drop = True)

# Write final output to csv
Day_count = pd.concat([Date,casCount,regCount,Temp], axis = 1)
Day_count.to_csv("DailyRidersTemp.csv", index = False)