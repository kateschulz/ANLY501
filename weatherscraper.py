# Scrape weather data using requests and BeautifulSoup

# Import Libraries
from bs4 import BeautifulSoup
import requests
import csv

# Create arrays for months and years we want to scrape
months = [i+1 for i in range(12)]
years = [2011, 2012, 2013, 2014, 2015]

# Define Weather function that scrapes the weather data
def Weather():
    
    # Create and Open CSV for Writing    
    csvName = "Weather.csv"
    csvFile = open(csvName, "wt")
    weatherwriter = csv.writer(csvFile, delimiter=',')
    
    # Write in Heading
    weatherwriter.writerow(['Year', 'Month', 'Day of Month', 'High Temp', 'Avg Temp', 'Low Temp', 'High Dew', 'Avg Dew', 'Low Dew', 
                            'High Humidity', 'Avg Humidity', 'Low Humidity', 'High SLP', 'Avg SLP', 'Low SLP', 
                            'High Vis', 'Avg Vis', 'Low Vis', 'High Wind', 'Avg Wind', 'Low Wind', 
                            'Precip', 'Events'])
    
    # Loop through the months and years & scrape and write the data into the CSV
    for year in years: 
        for month in months: 
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
