#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 13:30:28 2018

@author: marmuse
"""

import numpy as np
import matplotlib.pyplot as plt
import sys, os
from scipy.constants import k, e

sys.path.append('../backend/')

from solve_and_post_proc import solve
from diff_generator import gen_diff
from objects_generator import generate_all_objects

verbose = True
#verbose = False

# Choose gas
gas = 'xenon'

#%% Generate the differential equations

gen_diff('input_{}.txt'.format(gas))


#%% Create thruster, chemistry and parameters objects by reading the input file
my_objects = generate_all_objects('input_{}.txt'.format(gas))

thruster = my_objects[0]
params = my_objects[1]
chem = my_objects[2]
init = chem.init_vector
             
#%% Create set for running parametric

results = []
powers = np.arange(100,600,10)

for power in powers:
    params.Pabs = power / thruster.volume()
    results.append(solve(thruster, params, chem, init, temporal=False).values.y[-1])
    init = solve(thruster, params, chem, init, temporal=False).values.y[-1]
    
#%% Analyze
    
n_e   = [res[0] for res in results]
n_Xe  = [res[1] for res in results]
n_Xe_p  = [res[2] for res in results]
Te    = [res[3] for res in results]
Tg    = [res[4] for res in results]


#%% Initial plots wrt absorbed power

fig, ax = plt.subplots()
ax.plot(powers, n_e, label=r'n$_e$')
ax.plot(powers, n_Xe_p, label=r'n$_{Xe^+}$')
ax.plot(powers, n_Xe, label=r'n$_{Xe}$')
ax.set_yscale('Log')
ax.set_xlabel('Power absorbed (W)')
ax.set_ylabel('Densities (m-3)')
ax.legend(loc='best')

fig, ax = plt.subplots()
ax.plot(powers, Te, label=r'T$_e$')
ax.set_xlabel('Power absorbed (W)')
ax.set_ylabel('Te (eV)')
ax.legend(loc='best')


