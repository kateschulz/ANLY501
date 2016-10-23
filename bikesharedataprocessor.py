# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:22:38 2016

@author: eshope
"""

################################################
# Version Notes
# This file is using Python 3.5
# Anaconda updated 10/22/16
# Some functions require Pandas version 0.18.1
################################################

# Import libraries
import pandas as pd

# Read in the bikeshare data to dataframes - WILL NEED TO CHANGE TO FULL DATA!!
Q3_2015 = pd.read_csv("2015-Q3-cabi-trip-history-data-START.csv", parse_dates=True, infer_datetime_format=True, keep_date_col=True)
Q4_2015 = pd.read_csv("2015-Q4-Trips-History-Data-START.csv", parse_dates=True, infer_datetime_format=True, keep_date_col=True)
Q1_2016 = pd.read_csv("2016-Q1-Trips-History-Data-START.csv", parse_dates=True, infer_datetime_format=True, keep_date_col=True)
Q2_2016 = pd.read_csv("2016-Q2-Trips-History-Data-START.csv", parse_dates=True, infer_datetime_format=True, keep_date_col=True)

# Rename / reorder / split columns, etc. to allow dataframes to be concatenated
Q3_2015 = Q3_2015.rename(index=str, columns={"Bike #": "Bike number"})
Q4_2015 = Q4_2015.rename(index=str, columns={"Bike #": "Bike number"})
Q1_2016 = Q1_2016.rename(index=str, columns={"Member Type": "Member type"})
Q2_2016 = Q2_2016.rename(index=str, columns={"Account type": "Member type"})

# Merge the dataframes 
frames = [Q3_2015, Q4_2015, Q1_2016, Q2_2016]
all_bikeshare_data = pd.concat(frames, ignore_index=True)

# Define function for splitting the date columns into date and time columns
def SplitDateTime(dataframe):
    
    # Convert start and end dates into datetime objects    
    dataframe.loc[:,('Start date')] = pd.DatetimeIndex(dataframe.loc[:,('Start date')])
    dataframe.loc[:,('End date')] = pd.DatetimeIndex(dataframe.loc[:,('End date')])
    
    # Split start date and end date into start and end dates and times
    # Credit for this method: http://stackoverflow.com/a/24813856
    dataframe['Start time'], dataframe['Start date'] = dataframe['Start date'].apply(lambda x:x.time()), dataframe['Start date'].apply(lambda x:x.date())
    dataframe['End time'], dataframe['End date'] = dataframe['End date'].apply(lambda x:x.time()), dataframe['End date'].apply(lambda x:x.date())

# Run SplitDateTime function on all_bikeshare_data
SplitDateTime(all_bikeshare_data)

# Convert start date into datetime objects  
all_bikeshare_data.loc[:,('Start date')] = pd.DatetimeIndex(all_bikeshare_data.loc[:,('Start date')])

# Create new columns for the start day of week, start year, start month, start day, and month+year
all_bikeshare_data['Start Day of Week'] = all_bikeshare_data['Start date'].dt.weekday_name
all_bikeshare_data['Start Day'] = all_bikeshare_data['Start date'].dt.day
all_bikeshare_data['Start Month'] = all_bikeshare_data['Start date'].dt.month
all_bikeshare_data['Start Year'] = all_bikeshare_data['Start date'].dt.year
all_bikeshare_data['Start Month-Year'] = all_bikeshare_data['Start Month'].astype(str).str.cat(all_bikeshare_data['Start Year'].astype(str), sep='-')

# Create dataframe with trips per day
# Credit: Method for turning groupby object to dataframe from http://stackoverflow.com/a/10374456
trips_per_day = pd.DataFrame({'Number of Trips' : all_bikeshare_data.groupby( [ "Start date" ] ).size()}).reset_index()

# Add day of week into daily trip dataframe
trips_per_day['Day of Week'] = trips_per_day['Start date'].dt.weekday_name

# Determine number of trips each month & convert to dataframe
trips_per_month = pd.DataFrame({'Number of Trips' : all_bikeshare_data.groupby( [ "Start Month", "Start Year" ] ).size()}).reset_index()