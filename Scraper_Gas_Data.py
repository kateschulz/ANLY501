# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:32:25 2016

@author: kateschulz
"""

from bs4 import BeautifulSoup
import requests
import csv

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
 
    

