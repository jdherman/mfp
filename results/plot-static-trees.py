import numpy as np
import matplotlib.pyplot as plt
import pickle
# from tree import *
# from opt import *
# import folsom
import pandas as pd

gwcap = 0.5
ftype = 'actual'
seed = 5

snapshots = pickle.load(open('%s/snapshots-forecast-%s-gw%0.1fTAF-seed-%d.pkl' % (ftype,ftype,gwcap,seed), 'rb'))
P = snapshots['best_P'][-1]
print str(P)
P.graphviz_export('tree-ensemble-best.svg')
