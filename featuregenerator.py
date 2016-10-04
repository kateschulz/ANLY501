# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 07:14:11 2016

@author: eshope
"""

# Import libraries
import datetime
import pandas as pd

# Read in weather CSV
DataFrame = pd.read_csv("Weather.csv", sep = ',')

# Initialize a list to store days of week
dayOfWeek = []

# Determine day of week for each date & append to dayOfWeek list
for i in range(0, len(DataFrame)):
    year = DataFrame.iloc[i]['Year']    
    month = DataFrame.iloc[i]['Month']
    day = DataFrame.iloc[i]['Day of Month']
    dayOfWeek.append(datetime.datetime(year, month, day).strftime("%A"))

# Append dayOfWeek list to data frame
DataFrame['Day of Week'] = dayOfWeek

# Initialize a list to store binary precipitation
binaryPrecip = []

# Define function for checking if a string is a float
# Source: http://stackoverflow.com/questions/5956240/check-if-string-is-a-real-number
def isfloat(str):
    try: 
        float(str)
    except ValueError: 
        return False
    return True

# Determine yes (1) or no (0) for precipitation for each date & append to binaryPrecip list
for i in range(0, len(DataFrame)):
    precip = DataFrame.iloc[i]['Precip'] 
    if isfloat(precip) == False:
        binaryPrecip.append(DataFrame.iloc[i]['Precip'])
    else:
        precip = float(precip)  
        if precip <= 0:
            binaryPrecip.append(0)
        else:
            binaryPrecip.append(1)
        
# Append binaryPrecip list to data frame
DataFrame['Binary Precipitation'] = binaryPrecip

# Initialize a list to store the temp category/bin
tempCategory = []

# Determine category for each avg temp & append to tempCategory list
for i in range(0, len(DataFrame)):
    avgTemp = DataFrame.iloc[i]['Avg Temp']    
    
    if avgTemp.isnumeric() == True:
        if int(avgTemp) < 35:
            tempCategory.append(1)
        elif int(avgTemp) < 50:
            tempCategory.append(2)        
        elif int(avgTemp) < 60:
            tempCategory.append(3)     
        elif int(avgTemp) < 80:
            tempCategory.append(4)     
        else:
            tempCategory.append(5) 
    else:
        tempCategory.append(None)

# Append dayOfWeek list to data frame
DataFrame['Temp Category'] = tempCategory

# Write dataframe to CSV
DataFrame.to_csv("WeatherWithFeatures.csv", index=False)