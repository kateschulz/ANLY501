# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 22:39:01 2016

@author: kateschulz
"""
# This file runs one-way ANOVA, t-test, and multiple linear regression

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats

# Read data and define attributes for tests
Q1_2016 = pd.read_csv("/Users/kateschulz/Desktop/2016-Q1-Trips-History-Data-START.csv")

Duration = Q1_2016["Duration (ms)"]
StartStat = Q1_2016["Start station"]
StartNum = Q1_2016["Start station number"]
EndNum = Q1_2016["End station number"]

# Ordinary least squares model 
# Note: The response variable must be an int field
mod = ols('Duration ~ StartStat', data=Q1_2016).fit()

# One-way ANOVA computation, returns (sum squares, degrees freedom, F-statistic, and p-value)
anova = sm.stats.anova_lm(mod, typ=2)
print(anova)

# T-test computations, returns (t-statistic, p-value)
# Note: This has to be run on int fields.
ttest = stats.ttest_ind(StartNum, EndNum)
print (ttest)

# Set up data for multiple linear regression
x = Q1_2016[["Start station number", "End station number"]]
y = Q1_2016["Duration (ms)"]

# Run multiple linear regression
x = sm.add_constant(x)
est = sm.OLS(y, x).fit()

# get output from multiple linear regression
print(est.summary())
