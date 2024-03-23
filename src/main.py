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

# parsed_data = StrainProcess(raw_data, test_num, sample_dimensions)

# modulus = ModulusProcess(parsed_data, test_num)

# yield_strength = YieldProcess(parsed_data, test_num, modulus)
# ultimate_strength = UltimateProcess(parsed_data, test_num)

# print("Poisson's Ratio:")
# print(modulus[1]/modulus[2])

# print(parsed_data)
# print("Analysis Complete...")
# print("=========================================")

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

    