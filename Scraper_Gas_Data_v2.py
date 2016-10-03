# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:32:25 2016

@author: kateschulz
"""

from bs4 import BeautifulSoup
import pandas
import requests
import csv

#This function scrapes gas price data from an EIA table and writes it to a csv.
def GasPrices():
# We define the URL we will scrape the data from.
    url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=emm_epmru_pte_nus_dpg&f=m"
    page = requests.get(url)
    
# Using BeautifulSoup, we find the table we want within the html code and pull the records.
    soup = BeautifulSoup(page.text, "xml")
    table = soup.findAll("table")[5]
    all_TR = table.findAll("tr")
    
# We create the csv file we will write the data to. 
    csvName = "GasPrices.csv"
    csvFile = open(csvName,"wt")
    gaspricewriter = csv.writer(csvFile, delimiter = ',')
    gaspricewriter.writerow(['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    
# We populate the csv with data from the table and close the file.     
    for nextTR in all_TR:
        csvRow = []
        for nextTD in nextTR.findAll("td"):
            csvRow.append(nextTD.text.strip())
        gaspricewriter.writerow(csvRow)  
        
# We close the csv file.        
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
 
    

