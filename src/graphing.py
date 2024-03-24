"""
Functions related to plotting results
"""
# IMPORTS
#####################
# Dependancies
from scipy import io
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import os


def StrainGraph(data: pd.DataFrame, test: str, save: bool):
    '''
    PLots the strain graphs.

    Parameters:
    -----------   
    data : pd.DataFrame
        data from sensors
    test : str
        which test
    save : bool
        save graphs or not
    '''

    for n in range(1,5):

        params = {'mathtext.default': 'regular' }          
        plt.rcParams.update(params)
        plt.rcParams.update({'font.size': 12})
            
        print(" Generating " + test + " strain plots..")

        strain = -(data[f'SG{n}'])
        force = -(data.MTS_F)

        plt.plot(strain, force, color = 'r')

        
        plt.title(f'Al Beam, Gauge {n}: Force vs Strain')
        plt.ylabel('MTS Force (N)')
        plt.xlabel('Recorded Strain (mm/mm)')
        plt.ticklabel_format(axis='x', scilimits=[-3, 3])
        plt.ticklabel_format(axis='y', scilimits=[-3, 3])
        plt.grid()

        if save:
            os.makedirs(f'results/{test}-graphs/', exist_ok=True)
            plt.savefig(f'results/{test}-graphs/SG{n}_strain.png')
        plt.show()
        plt.clf()
    

def DisplacementGraph(data: pd.DataFrame, test: str, save: bool):
    '''
    PLots the strain graphs.

    Parameters:
    -----------   
    data : pd.DataFrame
        data from sensors
    test : str
        which test to plot
    save : bool
        save graphs or not
    '''

    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 10})

    force = -(data['MTS_F'])

    max_force = max(force)
    mf_ind = force.to_list().index(max_force)
    # straight_ind = data['SG_2'].iloc[>0.2e-4]

    max_d = []

    sensor = ['MTS_d', 'Actual_LD']

    for s in sensor: 
        
        disp = -(data[s])

        if s == 'Actual_LD':
            if test == 'AlBeam-3pnt':
                disp = disp - disp[100]
            elif test == 'AlBeam-4pnt':
                disp = disp - disp[0]
            else:
                disp = disp - disp[9 if test == '3D' else 0]

        max_disp = disp[mf_ind]
        max_d.append(max_disp)

        # plt.style.use('dark_background')

        plt.plot(disp, force)

    plt.scatter(max_d[0], max_force, marker='o')
    plt.scatter(max_d[1], max_force, marker='o')

    location = 'lower right' if test.startswith("AlB") else 'upper left'

    plt.legend(['MTS Data', f'Laser Data', f'MTS Max Def = {round(max_d[0], 2)} mm', f'Laser Max Def = {round(max_d[1], 2)} mm'], loc = location)
    if not test.startswith('AlB'):
        plt.text(1.5, 100, f'Max Loading: {max_force} N', style='italic', bbox={'alpha': 0.5, 'pad': 7})
    plt.title(f'{test} Beam: Force vs Deflection')
    plt.ylabel('MTS Force (N)')
    plt.xlabel('Center Deflection (mm)')
    plt.grid()
    plt.ticklabel_format(axis='y', scilimits=[-3, 3])


    if save:
        os.makedirs(f'results/{test}-graphs/', exist_ok=True)
        plt.savefig(f'results/{test}-graphs/{test}_disp.png')
    plt.show()
    plt.clf()
