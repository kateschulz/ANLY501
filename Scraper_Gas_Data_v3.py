# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:32:25 2016

@author: kateschulz
"""

from bs4 import BeautifulSoup
import pandas
import requests
import csv
import numpy

#This function scrapes gas price data from an EIA table and writes it to a csv.
def GasPrices():
    csvName = "GasPrices.csv"
    url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=emm_epmru_pte_nus_dpg&f=m"
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, "xml")
    
    table = soup.findAll("table")[5]
    all_TR = table.findAll("tr")
    csvFile = open(csvName,"wt")
    gaspricewriter = csv.writer(csvFile, delimiter = ',')
    gaspricewriter.writerow(['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    
    
    for nextTR in all_TR:
        csvRow = []
        for nextTD in nextTR.findAll("td"):
            csvRow.append(nextTD.text.strip())
        gaspricewriter.writerow(csvRow)
        
    csvFile.close()
     
GasPrices()


# This function corrects formatting issues with the gas price data. Specifically,
# we want to create a new csv with three columns: year, month, and average gas price.
def FixDataFormat():

# Importing csv created in GasPrices() ### ISSUE: The file is downloaded and called ###
    dataframe = pandas.read_csv('/Users/kateschulz/Documents/GasPrices.csv', sep = ',')
# The first 27 rows of the file contain the gas price data from 1990 to 2016
    dataframe = dataframe[0:27]
# We transpose this file to help with creating new Average Price column (see below)
    transdataframe = dataframe.T

# We instantiate a new dataframe to hold our re-formatted data.
    columns = ['Year','Month','Average Price']
    index = list(range(324))
    df = pandas.DataFrame(index=index, columns=columns)
    df = df.fillna(0) 

# We care about the years 1990 to 2016 with all months included.
    years = [1990+x for x in range(0,27)]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# We create an array of the years 1990 to 2016, with each year repeating 12 times
# (once for each month). 
    NewYear = []
    for x in range(0,27):
        for y in range(0,12):
            NewYear.append(years[x])
            
# We create an array of the months with each cycle repeating 27 times (once for each 
# year in 1990 through 2016).        
    NewMonth = []
    for x in range(0,27):
        for y in range(0,12):
            NewMonth.append(months[y]) 

# We used our transposed dataframe to create an array of the average gas prices 
# listed consecutively each month Jan. through Dec. and each year 1990 through 2016.
    AveragePrice = []
    for x in range(0,27):
        for y in range(1,13):
            AveragePrice.append(transdataframe[x][y])

# We populate our new dataframe with the arrays we have created for Year, Month,
# and Average Price.     
    df['Year'] = NewYear
    df['Month'] = NewMonth
    df['Average Price'] = AveragePrice

# We write a new csv with our re-formatted data.
    NewFile = "GasPriceFormat.csv"
    df.to_csv(NewFile) 
    
FixDataFormat()  
 

# This function checks the cleanliness of the gas price data. It counts the
# number of invalid records and divides it by the total number of records, producing
# a "cleanliness percentage." The lower the percentage, the cleaner the data.
def UnCleanlinessScore():

# We want to check for the following data quality issues for Averge Prices:
# 1) Null or 0 records
# 2) Non-numeric records 
# 3) Records outside the range of $0.50 to $5
# If any of the three criteria are violated, the record should either be eliminated
# or examined more closely.

# We import the csv created in FixDataFormat() ### ISSUE: The file is downloaded and called ###
    dataframe = pandas.read_csv('/Users/kateschulz/Documents/GasPriceFormat.csv', sep = ',')
    totalRecords = len(dataframe["Average Price"])

# TEST 1
# We test for Null or 0 records
    nullCount = dataframe["Average Price"].isnull()
    test1 = len(dataframe[nullCount])

# TEST 2
# We test for non-numeric records by creating a true/false dataframe and checking
# that all values in the Average Price column are true (i.e. are numbers).
    numeric = dataframe.applymap(numpy.isreal)
    nonNumCount = numeric["Average Price"] != True
    test2 = len(numeric[nonNumCount])
    
# TEST 3
# We test for records outside of a normal range for gas prices ($0.50 to $5).
    tooLow = dataframe["Average Price"] <= 0.5
    tooHigh = dataframe["Average Price"] >= 5
    test3 = len(dataframe[tooLow]) + len(dataframe[tooHigh])
 
# We compile the total number of invalid records and get our final score.
    totalInvalid = test1 + test2 + test3 
    score = (totalInvalid/totalRecords)*100
    print(score)

UnCleanlinessScore()
    

