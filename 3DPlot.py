# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 22:39:00 2016

@author: kateschulz
"""
# This file generates a 3D plot of a multiple linear regression
# with one response variable and two predictor variables (all numeric)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# NOTE : We cannot have spaces in the dataframe headings
Q1_2016 = pd.read_csv("/Users/kateschulz/Desktop/2016-Q1-Trips-History-Data-START.csv")
Q1_2016 = Q1_2016.rename(columns={"Start station number": "Startstationnumber"})
Q1_2016 = Q1_2016.rename(columns={"End station number": "Endstationnumber"})

# Set up data for multiple linear regression
x = Q1_2016[["Startstationnumber", "Endstationnumber"]]
y = Q1_2016["Duration (ms)"]

# Run multiple linear regression
x = sm.add_constant(x)
est = sm.OLS(y, x).fit()

# Create the 3d plot
xx1, xx2 = np.meshgrid(np.linspace(x.Startstationnumber.min(), x.Startstationnumber.max(), 100),
                       np.linspace(x.Endstationnumber.min(), x.Endstationnumber.max(), 100))

# plot the hyperplane by evaluating the parameters on the grid
Z = est.params[0] + est.params[1] * xx1 + est.params[2] * xx2

# create 3D axes
fig = plt.figure(figsize=(12, 8))
ax = Axes3D(fig, azim=-115, elev=15)

# plot hyperplane
surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

# plot data points 
resid = y - est.predict(x)
ax.scatter(x[resid >= 0].Startstationnumber, x[resid >= 0].Endstationnumber, y[resid >= 0], color='black', alpha=1.0)
ax.scatter(x[resid < 0].Startstationnumber, x[resid < 0].Endstationnumber, y[resid < 0], color='black', alpha=1.0)

# set axis labels
ax.set_xlabel('Start')
ax.set_ylabel('End')
ax.set_zlabel('Duration')

plt.show()