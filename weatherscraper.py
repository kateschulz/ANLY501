# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 14:53:17 2016

@author: eshope
"""

# Scrape weather data using requests and BeautifulSoup

# Import Libraries
from bs4 import BeautifulSoup
import requests
import csv

# Create arrays for months and years we want to scrape
months = [i+1 for i in range(12)]
years = [i for i in range(2000,2017)]

# Define Weather function that scrapes the weather data
def Weather():
    
    # Create and Open CSV for Writing    
    csvName = "Weather.csv"
    csvFile = open(csvName, "wt")
    weatherwriter = csv.writer(csvFile, delimiter=',')
    
    # Write in Heading
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

# Run the weather function to collect the data!
Weather()
