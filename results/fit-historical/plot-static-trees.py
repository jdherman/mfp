import numpy as np
import matplotlib.pyplot as plt
import pickle
from ptreeopt.tree import *
# from opt import *
# import folsom
import pandas as pd

# Historical best fit
file = 'snapshots-s4-fit-storage-rmse.pkl'

snapshots = pickle.load(open(file, 'rb'), encoding='latin1')
P = snapshots['best_P'][-1]
P.graphviz_export('hist-fit-storage.svg')

# snapshots = pickle.load(open('hist-opt/snapshots-depth-4-seed-8.pkl', 'rb'))
# P = snapshots['best_P'][-1]
# P.graphviz_export('../figs/fig-4-hist-results/hist-opt.svg')

