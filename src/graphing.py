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
    pos = [28,5,40,65]
    I = 1457918.40
    E = 72000 
    ind = [3, 1, 2, 4]  # for correcting the sequence

        # 1-->3
        # 2-->1
        # 3-->2
        # 4-->4
    
    for n in range(0,4):

        i = ind[n]

        params = {'mathtext.default': 'regular' }          
        plt.rcParams.update(params)
        plt.rcParams.update({'font.size': 12})
            
        print(" Generating " + test + " strain plots..")

        strain = (data[f'SG{n+1}'])
        force = -(data.MTS_F)
        num = 2 if test.endswith('3pnt') else 4
        e_xx_theor = -1*force*170*pos[n]/(num*E*I)

        plt.plot(force, strain, color = 'r')
        plt.plot(force, e_xx_theor)

        
        plt.title(f'{test}, Gauge {i}: Strain vs Force')
        plt.legend(['experimental','theoretical'])
        plt.xlabel('MTS Force (N)')
        plt.ylabel('Recorded Strain (mm/mm)')
        # plt.gca().set_xlim(0, f_lim)
        # plt.gca().set_ylim(5, 0)  
        plt.ticklabel_format(axis='x', scilimits=[-3, 3])
        plt.ticklabel_format(axis='y', scilimits=[-3, 3])
        plt.grid()

        if save:
            os.makedirs(f'results/{test}-graphs/', exist_ok=True)
            plt.savefig(f'results/{test}-graphs/SG{i}_strain.png')
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

        if s == 'MTS_d':
            if test == 'AlBeam-3pnt':
                disp = disp - disp[65]
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
