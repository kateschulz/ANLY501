# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 19:56:03 2016

@author: eshope
"""

# Import libraries
import requests
import pandas as pd
import csv

# Function for acquiring Census Tract and State data for each 
# Bikeshare station from Census Geocoding API
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
    

CensusTracts()