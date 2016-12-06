# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 17:49:09 2016

@author: kateschulz
"""

import pandas as pd

# Import all bikeshare trips 
all_bikeshare_data = pd.read_csv("BikeshareAllDatesSplit.csv")
weather_data = pd.read_csv("WeatherWithFeatures.csv")

# Left join bikeshare and weather data on common fields
complete = pd.merge(all_bikeshare_data, weather_data, how='left', 
                    on=['Month','Day of Month'])

# Group trips by each month
groups = pd.DataFrame({'count' : complete.groupby( 
                    ['Month','Member type'] ).size()}).reset_index()

# Group the casual trips for each month
casTrips = groups[groups["Member type"] == "Casual"] 

# Set up casual trip count for final output
casCount = casTrips.loc[:, ["count"]]
casCount = casCount.reset_index(drop = True)
casCount = casCount.rename(columns={'count': 'Casual'})

# Group the registered trips for each month
regTrips = groups[groups["Member type"] == "Registered"]

# Set up registered trip count for final output
regCount = regTrips.loc[:, ["count"]]
regCount = regCount.reset_index(drop = True)
regCount = regCount.rename(columns={'count': 'Registered'})

# Input all dates as Month-Year
dates = ['Jul-15','Aug-15','Sep-15','Oct-15','Nov-15','Dec-15',
       'Jan-16','Feb-16','Mar-16','Apr-16','May-16','Jun-16']
Date = pd.DataFrame(dates)
Date.columns = ["Date"]

# Input all monthly average temps
temps = [82, 79, 75, 59, 54, 51, 35, 40, 54, 57, 64, 76]
AvgTemp = pd.DataFrame(temps)
AvgTemp.columns = ['Avg Temp']

# Write final output to csv
Month_count = pd.concat([Date,casCount,regCount,AvgTemp], axis = 1)
Month_count.to_csv("MonthlyRidersTemp.csv", index = False)