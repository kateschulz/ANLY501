# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:03:34 2016

@author: kateschulz
"""

# This file reads in a Bikeshare data csv and performs the apriori assocation rule

import pandas as pd
from fim import apriori

# Read in Bikeshare data (need to not hardcode this)
Q1_2016 = pd.read_csv("/Users/kateschulz/Desktop/2016-Q1-Trips-History-Data-START.csv")

# Delete columns irrelevant for apriori (all but the Start station and End station)
delcols = ["Duration (ms)", "Start date", "End date", "Start station number", "End station number","Bike number", "Member Type"]
for col in delcols:
    del Q1_2016[col] 

# Save dataframe to .txt file
NewFile = "AprioriTest2.txt"
Q1_2016.to_csv(NewFile, sep = ',', header=False, index=False)

# Read the .txt file into a matrix
matrix = []
with open('AprioriTest2.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            matrix.append(list(map(str, line.split(','))))

# Call apriori for the association rule 
minsup = [10,30,40]
minconf = [20,30,40]
for x in range(0,3):
    for y in range(0,3):
        print("minsup =",minsup[x])
        print("minconf =",minconf[y])
        print(apriori(matrix, target = 'r', supp = minsup[x], conf = minconf[y]))





