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
        cleanliness.write("GAS PRICES\n")
    
    # Import the csv created in GasPrices() and count total records
    gaspricedataframe = pd.read_csv("GasPrices.csv", sep = ',')
    totalRecords = len(gaspricedataframe["Gas Price"])
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Total gas price records: " + str(totalRecords) + "\n")
    
    # Count null records
    nullRecords = gaspricedataframe["Gas Price"].isnull()
    nullRecordsCount = len(gaspricedataframe[nullRecords])
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Number of null records: " + str(nullRecordsCount) + "\n")
    
    # Count non-numeric values
    numeric = gaspricedataframe.applymap(np.isreal)
    nonNumeric = numeric["Gas Price"] != True
    nonNumericCount = len(numeric[nonNumeric])
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Number of non-numeric values: " + str(nonNumericCount) + "\n")
    
    # Count values outside normal range
    tooLow = gaspricedataframe["Gas Price"] <= 0.5
    tooHigh = gaspricedataframe["Gas Price"] >= 5
    outsideNormalCount = sum(tooLow) + sum(tooHigh)
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("Number of records <= 0.5 or >= 5: " + str(outsideNormalCount) + "\n")
    
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
        cleanliness.write("WEATHER DATA\n")
    
# Create function to check and describe Bikeshare station data (un)cleanliness
def BikeshareUnclean():

    # Prepare to write in data cleanliness info
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("BIKESHARE STATION DATA\n")

# Create function to check and describe Census data (un)cleanliness
def CensusUnclean():

    # Prepare to write in data cleanliness info
    with open("data_cleanliness.txt", 'a') as cleanliness:
        cleanliness.write("CENSUS DATA\n")
        
# Call cleanliness assessment functions
GasPriceUnclean()
WeatherUnclean()
BikeshareUnclean()
CensusUnclean()