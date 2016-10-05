# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:01:15 2016

@author: eshope
"""

import pandas as pd
import numpy as np

# Set up a file for writing in data cleanliness info
with open("data_cleanliness.txt", 'w') as cleanliness:
    cleanliness.write("Shope Schulz Data Cleanliness Checks and Scores\n\n")

# Create function to check and describe gas price data (un)cleanliness
def GasPriceUnclean():

    # Prepare to write in data cleanliness info
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("**GAS PRICES**\n")
    
    # Import the csv created in GasPrices() and count total records
    dataframe = pd.read_csv("GasPrices.csv", sep = ',')
    totalRecords = len(dataframe["Gas Price"])
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Total gas price records: " + str(totalRecords) + "\n\n")
    
    # Count null records
    nullRecords = dataframe["Gas Price"].isnull()
    nullRecordsCount = len(dataframe[nullRecords])
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Number of missing values: " + str(nullRecordsCount) + "\n")
        cleanliness.write("Fraction of missing values: " + str(nullRecordsCount/totalRecords) + "\n")
    
    # Count non-numeric values
    numeric = dataframe.applymap(np.isreal)
    nonNumeric = numeric["Gas Price"] != True
    nonNumericCount = len(numeric[nonNumeric])
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Number of noise values: " + str(nonNumericCount) + "\n")
        cleanliness.write("Fraction of noise values: " + str(nonNumericCount/totalRecords) + "\n")
    
    # Count values outside normal range
    tooLow = dataframe["Gas Price"] <= 0.5
    tooHigh = dataframe["Gas Price"] >= 5
    outsideNormalCount = sum(tooLow) + sum(tooHigh)
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Number of records that don't make sense (too high or too low): " + str(outsideNormalCount) + "\n")
    
    # Sum total number of invalid records and get final score
    totalInvalid = nullRecordsCount + nonNumericCount + outsideNormalCount
    score = (totalInvalid/totalRecords)*100
    rounded_score = float("{0:.2f}".format(score))
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Total invalid records: " + str(totalInvalid) + "\n")
        cleanliness.write("Gas Price Data Score = " + str(totalInvalid) + "/" + str(totalRecords) + " = " + str(rounded_score) + "%\n\n")
    
# Create function to check and describe gas price data (un)cleanliness
def WeatherUnclean():
    
    # Prepare to write weather data
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("**WEATHER DATA**\n")
        
    # Import Weather.csv and count total records
    dataframe = pd.read_csv("Weather.csv", sep = ',')
    totalRecords = len(dataframe)
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Total records: " + str(totalRecords) + "\n\n")
    
    # Define function for checking if a string is a float
    # Source: http://stackoverflow.com/questions/5956240/check-if-string-is-a-real-number
    def isfloat(str):
        try: 
            float(str)
        except ValueError: 
            return False
        return True
    
    # Define columns for which we want to check cleanliness
    columns = ['Avg Temp', 'Avg Wind', 'Precip']
    
    for column in columns:
        
        # Count null records
        nullRecords = dataframe[column].isnull()
        nullRecordsCount = len(dataframe[nullRecords])
        
        # Count non-numeric values
        numeric = dataframe.applymap(isfloat)
        nonNumeric = numeric[column] != True
        nonNumericCount = len(numeric[nonNumeric])
            
        # Count total number of invalid records per attribute and get final scores
        totalInvalid = nullRecordsCount + nonNumericCount
        score = (totalInvalid/totalRecords)*100
        rounded_score = float("{0:.2f}".format(score))
        
        # Write scoring to file
        with open("data_cleanliness.txt", 'a') as cleanliness:
            cleanliness.write("Number of missing values for " + column + ": " + str(nullRecordsCount) + "\n")
            cleanliness.write("Fraction of missing values for " + column + ": " + str(nullRecordsCount/totalRecords) + "\n")
            cleanliness.write("Number of noise values for " + column + ": " + str(nonNumericCount) + "\n")
            cleanliness.write("Fraction of noise values for " + column + ": " + str(nonNumericCount/totalRecords) + "\n")
            cleanliness.write("Total invalid records for " + column + ": " + str(totalInvalid) + "\n")            
            cleanliness.write(column + " Score for " + column + " = " + str(totalInvalid) + "/" + str(totalRecords) + " = " + str(rounded_score) + "%\n\n")
    
# Create function to check and describe Bikeshare station data (un)cleanliness
def BikeshareUnclean():
    
    # Prepare to write in data cleanliness info
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("**BIKESHARE STATION DATA**\n")
    
    # Import CapitalBikeshareStationData.csv and count total records
    dataframe = pd.read_csv("CapitalBikeshareStationData.csv", sep = ',')
    totalRecords = len(dataframe)
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Total records: " + str(totalRecords) + "\n\n")
    
    # Define columns for which we want to check cleanliness
    columns = ['Station ID', 'Latitude', 'Longitude', 'Number of Bikes', 'Number of Empty Docks']
    
    for column in columns:
        
        # Count null records
        nullRecords = dataframe[column].isnull()
        nullRecordsCount = len(dataframe[nullRecords])
        
        # Count non-numeric records
        numeric = dataframe.applymap(np.isreal)
        nonNumeric = numeric[column] != True
        nonNumericCount = len(numeric[nonNumeric])
        
        # Count total number of invalid records per attribute and get final scores
        totalInvalid = nullRecordsCount + nonNumericCount
        score = (totalInvalid/totalRecords)*100
        rounded_score = float("{0:.2f}".format(score))
        
        # Write scoring to file
        with open("data_cleanliness.txt", 'a') as cleanliness:
            cleanliness.write("Number of missing values for " + column + ": " + str(nullRecordsCount) + "\n")
            cleanliness.write("Fraction of missing values for " + column + ": " + str(nullRecordsCount/totalRecords) + "\n")
            cleanliness.write("Number of noise values for " + column + ": " + str(nonNumericCount) + "\n")
            cleanliness.write("Fraction of noise values for " + column + ": " + str(nonNumericCount/totalRecords) + "\n")
            cleanliness.write("Total invalid records for " + column + ": " + str(totalInvalid) + "\n")            
            cleanliness.write(column + " Score for " + column + " = " + str(totalInvalid) + "/" + str(totalRecords) + " = " + str(rounded_score) + "%\n\n")
    
    # Define additional columns for which we want to check cleanliness
    columns2 = ['Name']
    
    for column in columns2:
        
        # Count null records
        nullRecords = dataframe[column].isnull()
        nullRecordsCount = len(dataframe[nullRecords])
        
        # Count total number of invalid records per attribute and get final scores
        totalInvalid = nullRecordsCount
        score = (totalInvalid/totalRecords)*100
        rounded_score = float("{0:.2f}".format(score))
        
        # Write scoring to file
        with open("data_cleanliness.txt", 'a') as cleanliness:
            cleanliness.write("Number of missing values for " + column + ": " + str(nullRecordsCount) + "\n")
            cleanliness.write("Fraction of missing values for " + column + ": " + str(nullRecordsCount/totalRecords) + "\n")
            cleanliness.write("Total invalid records for " + column + ": " + str(totalInvalid) + "\n")            
            cleanliness.write(column + " Score for " + column + " = " + str(totalInvalid) + "/" + str(totalRecords) + " = " + str(rounded_score) + "%\n\n")
    
# Create function to check and describe Census data (un)cleanliness
def CensusUnclean():
    
    # Prepare to write in data cleanliness info
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("**CENSUS DATA**\n")
        
    # Import BikeshareDataPlusCensus.csv and count total records
    dataframe = pd.read_csv("BikeshareDataPlusCensus.csv", sep = ',')
    totalRecords = len(dataframe)
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Total records: " + str(totalRecords) + "\n\n")
    
    # Define columns for which we want to check cleanliness
    columns = ['Census Tract']
    
    for column in columns:
        
        # Count null records
        nullRecords = dataframe[column].isnull()
        nullRecordsCount = len(dataframe[nullRecords])
        
        # Count non-numeric records
        numeric = dataframe.applymap(np.isreal)
        nonNumeric = numeric[column] != True
        nonNumericCount = len(numeric[nonNumeric])
        
        # Count total number of invalid records per attribute and get final scores
        totalInvalid = nullRecordsCount + nonNumericCount
        score = (totalInvalid/totalRecords)*100
        rounded_score = float("{0:.2f}".format(score))
        
        # Write scoring to file
        with open("data_cleanliness.txt", 'a') as cleanliness:
            cleanliness.write("Number of missing values for " + column + ": " + str(nullRecordsCount) + "\n")
            cleanliness.write("Fraction of missing values for " + column + ": " + str(nullRecordsCount/totalRecords) + "\n")
            cleanliness.write("Number of noise values for " + column + ": " + str(nonNumericCount) + "\n")
            cleanliness.write("Fraction of noise values for " + column + ": " + str(nonNumericCount/totalRecords) + "\n")
            cleanliness.write("Total invalid records for " + column + ": " + str(totalInvalid) + "\n")            
            cleanliness.write(column + " Score for " + column + " = " + str(totalInvalid) + "/" + str(totalRecords) + " = " + str(rounded_score) + "%\n\n")
    
    # Define additional columns for which we want to check cleanliness
    columns2 = ['State']
    
    for column in columns2:
        
        # Count null records
        nullRecords = dataframe[column].isnull()
        nullRecordsCount = len(dataframe[nullRecords])
        
        # Count total number of invalid records per attribute and get final scores
        totalInvalid = nullRecordsCount
        score = (totalInvalid/totalRecords)*100
        rounded_score = float("{0:.2f}".format(score))
        
        # Write scoring to file
        with open("data_cleanliness.txt", 'a') as cleanliness:
            cleanliness.write("Number of missing values for " + column + ": " + str(nullRecordsCount) + "\n")
            cleanliness.write("Fraction of missing values for " + column + ": " + str(nullRecordsCount/totalRecords) + "\n")
            cleanliness.write("Total invalid records for " + column + ": " + str(totalInvalid) + "\n")            
            cleanliness.write(column + " Score for " + column + " = " + str(totalInvalid) + "/" + str(totalRecords) + " = " + str(rounded_score) + "%\n\n")

    
# Call cleanliness assessment functions
GasPriceUnclean()
WeatherUnclean()
BikeshareUnclean()
CensusUnclean()
