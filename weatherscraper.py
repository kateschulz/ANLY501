from bs4 import BeautifulSoup
import requests
import csv


def Weather():
    csvName = "Weather.csv"
    url = "https://www.wunderground.com/history/airport/KDCA/2015/1/1/MonthlyHistory.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    table = soup.findAll("table")[3]
    All_TR = table.findAll("tr")[2:]
    csvFile = open(csvName, "wt")
    weatherwriter = csv.writer(csvFile, delimiter=',')
    weatherwriter.writerow(['Year', 'Month', 'Day of Month', 'High Temp', 'Avg Temp', 'Low Temp', 'High Dew', 'Avg Dew', 'Low Dew', 
                            'High Humidity', 'Avg Humidity', 'Low Humidity', 'High SLP', 'Avg SLP', 'Low SLP', 
                            'High Vis', 'Avg Vis', 'Low Vis', 'High Wind', 'Avg Wind', 'Low Wind', 
                            'Precip', 'Events'])
    for nextTR in All_TR:
        csvRow = []
        csvRow.append('2015')
        csvRow.append('Jan')
        for nextTD in nextTR.findAll("td"):
            csvRow.append(nextTD.text.strip())
        weatherwriter.writerow(csvRow)
    csvFile.close()


Weather()
