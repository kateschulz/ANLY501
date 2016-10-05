# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:02:26 2016

@author: eshope
"""

# Import Libraries
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np
import datetime

# Create function that will scrape gas prices, 
# input them with the appropriate year into a data frame, 
# and then print the data frame to a CSV
def GasPrices():
    
    # Create arrays for months and years we want to scrape
    months = [i+1 for i in range(12)]
    years = [i for i in range(1990,2017)]
    
    # Set up query & retrieve gas price data
    url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=emm_epmru_pte_nus_dpg&f=m"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "xml")
    table = soup.findAll("table")[5]
    all_TR = table.findAll("tr")
    
    # Put the gas prices into a list
    gaspricelist = []
    
    for nextTR in all_TR:
        for nextTD in nextTR.findAll("td", class_="B3"):
            gaspricelist.append(nextTD.text)
    
    # Set up months and years lists that correspond to the gas prices
    yearlist = []
    monthlist = []
    
    for year in years:
        for month in months:
            yearlist.append(year)
            monthlist.append(month)
    
    # Turn the lists into a data frame
    GasPriceDataFrame = pd.DataFrame.from_items([('Year', yearlist), 
                                                 ('Month', monthlist), 
                                                ('Gas Price', gaspricelist)])

    # Print the data frame to a CSV
    GasPriceDataFrame.to_csv("GasPrices.csv", index=False)
    
# Define Weather function that scrapes DC weather data for Jan 2000 - June 2016
def Weather():
    
    # Create arrays for months and years we want to scrape
    months = [i+1 for i in range(12)]
    years = [i for i in range(2000,2017)]
    
    # Create and open CSV for writing    
    csvName = "Weather.csv"
    csvFile = open(csvName, "wt")
    weatherwriter = csv.writer(csvFile, delimiter=',')
    
    # Write in heading
    weatherwriter.writerow(['Year', 'Month', 'Day of Month', 'High Temp', 'Avg Temp', 'Low Temp', 'High Dew', 'Avg Dew', 'Low Dew', 
                            'High Humidity', 'Avg Humidity', 'Low Humidity', 'High SLP', 'Avg SLP', 'Low SLP', 
                            'High Vis', 'Avg Vis', 'Low Vis', 'High Wind', 'Avg Wind', 'Max Gust', 
                            'Precip', 'Events'])
    
    # Loop through the months and years & scrape and write the data into the CSV
    for year in years: 
        for month in months: 
            if year == 2016 and month > 6:
                break
            url = "https://www.wunderground.com/history/airport/KDCA/" + str(year) + "/" + str(month) + "/1/MonthlyHistory.html"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            table = soup.findAll("table")[3]
            All_TR = table.findAll("tr")[2:]
            for nextTR in All_TR:
                csvRow = []
                csvRow.append(year)
                csvRow.append(month)
                for nextTD in nextTR.findAll("td"):
                    csvRow.append(nextTD.text.strip())
                weatherwriter.writerow(csvRow)
    
    # Close the file
    csvFile.close()

# Define dcBikeshare function that scrapes Capital Bikeshare station data
def dcBikeshare():
    
    # Create and Open CSV for writing    
    csvName = "CapitalBikeshareStationData.csv"
    csvFile = open(csvName, "wt")
    bikesharewriter = csv.writer(csvFile, delimiter=',')
    
    # Access the data and turn it into Beautiful Soup 
    url = "https://feeds.capitalbikeshare.com/stations/stations.xml"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    
    # Gather the data into variables
    myID = soup.find_all("id")
    myName = soup.find_all('name')
    myLat = soup.find_all("lat")
    myLong = soup.find_all("long")
    myNBBikes = soup.find_all("nbbikes")
    myNBEmptyDocks = soup.find_all("nbemptydocks")
    
    # Calculate # of Bikeshare stations we need to iterate over    
    numstations = len(soup.find_all("id"))
    
    # Write in heading
    bikesharewriter.writerow(['Station ID', 'Name', 'Latitude', 'Longitude', 'Number of Bikes', 'Number of Empty Docks'])
    
    # Iterate over # of stations -- 1 row = 1 station
    for i in range(0, numstations):
        
        csvRow = []

        for child in myID[i].children:
            csvRow.append(child)        
        for child in myName[i].children:
            csvRow.append(child)  
        for child in myLat[i].children:
            csvRow.append(child) 
        for child in myLong[i].children:
            csvRow.append(child)             
        for child in myNBBikes[i].children:
            csvRow.append(child)             
        for child in myNBEmptyDocks[i].children:
            csvRow.append(child)             
            
        bikesharewriter.writerow(csvRow)
    
    # Close the file
    csvFile.close()

# Define CensusTracts function for acquiring Census Tract and State data
# for each Bikeshare station from Census Geocoding API
def CensusTracts():

    # Read Bikeshare Station Data file to Pandas Data Frame (for accessing lats & longs)
    latlongFile = pd.read_csv("CapitalBikeshareStationData.csv")

    # Create and open CSV for writing    
    csvName = "BikeshareDataPlusCensus.csv"
    csvFile = open(csvName, "wt")
    censuswriter = csv.writer(csvFile, delimiter=',')
    
    # Write in heading
    censuswriter.writerow(['Station ID', 'Name', 'Latitude', 'Longitude', 'Number of Bikes', 'Number of Empty Docks', 'Census Tract', 'State'])
    
    # Loop through each of the stations
    for i in range(0, len(latlongFile)):

        # Setup parameters for API call including the lat & long from the data frame
        query_params = {'x': latlongFile.iloc[i]['Longitude'],
                        'y': latlongFile.iloc[i]['Latitude'],
                        'benchmark': 'Public_AR_Census2010',
                        'vintage': 'Census2010_Census2010',
                        'format': 'json'}    
        
        endpoint = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"

        response = requests.get(endpoint, query_params)
    
        # Get the json response and parse the Census Tract and State Name
        jtxt = response.json()
        myTract = jtxt['result']['geographies']['Census Tracts'][0].get('TRACT') 
        myState = jtxt['result']['geographies']['States'][0].get('NAME') 
        
        # Print the existing Bikeshare station data plus the Census Tract and State info to the file
        censuswriter.writerow([latlongFile.iloc[i]['Station ID'],
                               latlongFile.iloc[i]['Name'],
                                latlongFile.iloc[i]['Latitude'], 
                                latlongFile.iloc[i]['Longitude'], 
                                latlongFile.iloc[i]['Number of Bikes'], 
                                latlongFile.iloc[i]['Number of Empty Docks'], 
                                myTract, 
                                myState])                                                                                                                                                                              
    
    # Close the file
    csvFile.close()

# Run functions to collect data
Weather()
dcBikeshare()
CensusTracts()
GasPrices()

# Create function to generate features
def FeatureGen():
    
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
            binaryPrecip.append(None)
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

# Run feature generator
FeatureGen()

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