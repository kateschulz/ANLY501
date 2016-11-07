# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 17:49:01 2016

@author: kateschulz
"""
# This file runs a Gaussian Naive Bayes Classifier 

import pandas as pd
from sklearn.naive_bayes import GaussianNB

Q1_2016 = pd.read_csv("/Users/kateschulz/Desktop/2016-Q1-Trips-History-Data-START.csv")
gnb = GaussianNB()

# Data to train
StartNum = Q1_2016["Start station number"].to_frame()
#Data to predict
EndNum = Q1_2016["End station number"].to_frame()

# Naive Bayes computations
EndNum_pred = gnb.fit(StartNum, EndNum.values.ravel()).predict(StartNum)
print(EndNum_pred)

# Cross-validation of correctly predicted classifications
print("Number of mislabeled points out of a total %d points : %d"
      % (len(StartNum),(Q1_2016["End station number"]  != EndNum_pred).sum()))