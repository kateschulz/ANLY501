# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:48:22 2016

@author: eshope
"""

# Scrape Capital Bikeshare station info data using requests and BeautifulSoup

# Import Libraries
from bs4 import BeautifulSoup
import requests
import csv

# Define dcBikeshare function that scrapes Capital Bikeshare
def dcBikeshare():
    
    # Create and Open CSV for Writing    
    csvName = "CapitalBikeshareStationData.csv"
    csvFile = open(csvName, "wt")
    bikesharewriter = csv.writer(csvFile, delimiter=',')
    
    # Access the Data and Turn It Into Beautiful Soup 
    url = "https://feeds.capitalbikeshare.com/stations/stations.xml"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    
    # Gather the Data Into Variables
    myID = soup.find_all("id")
    myName = soup.find_all('name')
    myLat = soup.find_all("lat")
    myLong = soup.find_all("long")
    myNBBikes = soup.find_all("nbbikes")
    myNBEmptyDocks = soup.find_all("nbemptydocks")
    
    # Calculate the Number of Bikeshare Stations We Need to Iterate Over    
    numstations = len(soup.find_all("id"))
    
    # Write in Heading
    bikesharewriter.writerow(['Station ID', 'Name', 'Latitude', 'Longitude', 'Number of Bikes', 'Number of Empty Docks'])
    
    # Iterate Over the Number of Stations - Create Rows which Each Contain Data for One Station
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

# Run the dcBikeshare function to collect the data!
dcBikeshare()