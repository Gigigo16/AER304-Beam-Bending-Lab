"""
Main script for running all data processing and plotting.
    {Depenancies}: scipy, matplotlib, numpy, pandas
"""
# IMPORTS
#####################
# Dependancies
from scipy import io
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

# Custom Functions/libraies
from graphing import *
from analysis import *

# DEFINITIONS
########################

skip_rows = 22
cols = ['time', 'MTS_F', 'MTS_d', 'LD', 'SG1', 'SG2', 'SG3', 'SG4', 'Actual_LD', 'unk1', 'unk2']

test = 'AlBeam-4pnt'

# for reading to pd df
file_path = f"Data\Labview Data\{test}.txt"

print("=========================================")
print("Loading Data for 3D print...")
# print("=========================================")

# LOADING TEST DATA
##############################
raw_data = pd.read_csv(file_path, skiprows=skip_rows, sep = '\t')
raw_data.columns = cols

# PROCESSING DATA
########################
print("=========================================")
print("Beginning Analysis...")
print("=========================================")

# Analysis for theoretical I-beam deflections:
I = 1457918.40
E = 72000
L = 400
H = 76
b = 8.86

nx, ny = (L+1, H*2+1)
x = np.linspace(-L/2, L/2, nx)
y = np.linspace(-H/2, H/2, ny)
xv, yv = np.meshgrid(x, y)

# 3-pnt:
max_F3 = 17238.5017
M_max = max_F3*L/2
slope = M_max/(L/2)
M3 = M_max - slope*abs(x)
sig3_xx = -1*M3*yv/I
eps3_xx = sig3_xx/E
Q = b/2*(H**2/4 - yv**2)
sig3_xy = max_F3/2 * Q/I/b
eps3_xy = sig3_xy/E
eps3_xy[:,200:-1] = -1*eps3_xy[:,200:-1]
plt.contourf(xv, yv, sig3_xx)
plt.colorbar()
plt.show()


# 4-pnt:
max_F4 = 17806.9821
M4 = max_F4*140 # 400/2 - 120/2
sig4_xx = -M4*yv/I
eps4_xx = sig4_xx/E
Q = b/2*(H**2/4 - yv**2)
sig4_xy = max_F4/2 * Q/I/b
eps4_xy = sig4_xy/E
eps4_xy[:,200:-1] = -1*eps4_xy[:,200:-1]
plt.contourf(xv, yv, sig4_xx)
plt.colorbar()
plt.show()



print("Analysis Complete...")
print("=========================================")

# GRAPHING DATA
########################

save = True
# StrainGraph(parsed_data, test_num, sensor, modulus, yield_strength, ultimate_strength, save)
if test.startswith('AlB'):
    StrainGraph(raw_data, test, save)
DisplacementGraph(raw_data, test, save)
print("=========================================")

# print("Saving Data CSVs...")
# Saving data raw data to CSV

# find the ultimate yield 
# find poisson's ration

    