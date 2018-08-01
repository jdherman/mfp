import numpy as np
import matplotlib.pyplot as plt
import pickle
from mfp import MFPModel
from ptreeopt import PTreeOpt
import pandas as pd

best_seeds = {'Control,no_pulse': 21,
'Control,FERC': 4,
'Control,increase_rampdown': 4,
'Control,increase_rampdown_BN': 7,
'Treatment,no_pulse': 8,
'Treatment,FERC': 6,
'Treatment,increase_rampdown': 9,
'Treatment,increase_rampdown_BN': 0,
'OldFireModel_Extreme_Control,no_pulse': 9,
'OldFireModel_Extreme_Control,FERC': 29,
'OldFireModel_Extreme_Control,increase_rampdown': 9,
'OldFireModel_Extreme_Control,increase_rampdown_BN': 6,
'OldFireModel_Moderate_Control,no_pulse': 8,
'OldFireModel_Moderate_Control,FERC': 3,
'OldFireModel_Moderate_Control,increase_rampdown': 0,
'OldFireModel_Moderate_Control,increase_rampdown_BN': 6,
'OldFireModel_Extreme_Treatment,no_pulse': 0,
'OldFireModel_Extreme_Treatment,FERC': 6,
'OldFireModel_Extreme_Treatment,increase_rampdown': 9,
'OldFireModel_Extreme_Treatment,increase_rampdown_BN': 4,
'OldFireModel_Moderate_Treatment,no_pulse': 8,
'OldFireModel_Moderate_Treatment,FERC': 0,
'OldFireModel_Moderate_Treatment,increase_rampdown': 1,
'OldFireModel_Moderate_Treatment,increase_rampdown_BN': 0}

cols_to_save = ['dowy', 'SFMD', 'RFMD', 'QFMD', 'SHHL', 'RHHL',
       'QHHL', 'total_power']

vegscens = ['Control', 'Treatment',
            'OldFireModel_Extreme_Control',
            'OldFireModel_Moderate_Control',
            'OldFireModel_Extreme_Treatment',
            'OldFireModel_Moderate_Treatment']

for vegscen in vegscens:
  for envscen in ['no_pulse', 'FERC', 'increase_rampdown', 'increase_rampdown_BN']:
    
    model = MFPModel('mfp/data/mfp_data.csv', 
                      sd='1980-10-01', ed='2015-09-30', # end date for Phil's data
                      env_scenario=envscen,
                      veg_scenario=vegscen,
                      fit_historical=False)

    # need to know here which seed results in the best policy
    bestS = best_seeds['%s,%s' % (vegscen,envscen)]

    data = pickle.load(
      open('results/opt-historical/snapshots-s%d-%s-%s.pkl' % 
            (bestS,vegscen,envscen), 'rb'), encoding='latin1') # encoding important py3

    bestP = data['best_P'][-1]
    df = model.f(P=bestP, mode='simulation')
    df[cols_to_save].to_csv('results/timeseries/%s_%s.csv' % (vegscen,envscen))
    # power = df.total_power.resample('AS-OCT').sum().mean()/1000
    