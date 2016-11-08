# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:03:34 2016

@author: kateschulz
"""

# This file reads in a Bikeshare data csv and performs the apriori assocation rule

import pandas as pd
from fim import apriori

# Read in Bikeshare data (need to not hardcode this)
Q1_2016 = pd.read_csv("2016-Q1-Trips-History-Data.csv")
Q2_2016 = pd.read_csv("2016-Q2-Trips-History-Data.csv")
Q3_2015 = pd.read_csv("2015-Q3-cabi-trip-history-data.csv")
Q4_2015 = pd.read_csv("2015-Q4-Trips-History-Data.csv")

# Delete columns irrelevant for apriori (all but the Start station and End station)
# Q1 columns
delcols = ["Duration (ms)", "Start date", "End date", "Start station number", "End station number","Bike number", "Member Type"]
for col in delcols:
    del Q1_2016[col] 
    
# Q2 columns
delcols = ["Duration (ms)", "Start date", "End date", "Start station number", "End station number","Bike number", "Account type"]
for col in delcols:
    del Q2_2016[col]  

# Q3 columns
delcols = ["Duration (ms)", "Start date", "End date", "Start station number", "End station number","Bike #", "Member type"]
for col in delcols:
    del Q3_2015[col] 

# Q4 columns
delcols = ["Duration (ms)", "Start date", "End date", "Start station number", "End station number","Bike #", "Member type"]
for col in delcols:
    del Q4_2015[col] 

# Save dataframe to .txt file
NewFileQ1 = "AprioriTestQ1.txt"
Q1_2016.to_csv(NewFileQ1, sep = ',', header=False, index=False)

NewFileQ2 = "AprioriTestQ2.txt"
Q2_2016.to_csv(NewFileQ2, sep = ',', header=False, index=False)

NewFileQ3 = "AprioriTestQ3.txt"
Q3_2015.to_csv(NewFileQ3, sep = ',', header=False, index=False)

NewFileQ4 = "AprioriTestQ4.txt"
Q4_2015.to_csv(NewFileQ4, sep = ',', header=False, index=False)


# Read the .txt file into a matrix
matrixQ1 = []
with open('AprioriTestQ1.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            matrixQ1.append(list(map(str, line.split(','))))
            
matrixQ2 = []
with open('AprioriTestQ2.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            matrixQ2.append(list(map(str, line.split(','))))
            
matrixQ3 = []
with open('AprioriTestQ3.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            matrixQ3.append(list(map(str, line.split(','))))
            
matrixQ4 = []
with open('AprioriTestQ4.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            matrixQ4.append(list(map(str, line.split(','))))

# Call apriori for the association rule 
minsup = [3,4,5]
minconf = 3
for x in range(0,3):
    print("minsup =",minsup[x])
    print("minconf =",minconf)
    print("Q1:",apriori(matrixQ1, target = 'r', zmin=2, supp = minsup[x], conf = minconf))
    print("Q2:",apriori(matrixQ2, target = 'r', zmin=2, supp = minsup[x], conf = minconf))
    print("Q3:",apriori(matrixQ3, target = 'r', zmin=2, supp = minsup[x], conf = minconf))
    print("Q4:",apriori(matrixQ4, target = 'r', zmin=2, supp = minsup[x], conf = minconf))







