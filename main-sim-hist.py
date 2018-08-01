import numpy as np
import matplotlib.pyplot as plt
import pickle
from mfp import MFPModel
from ptreeopt import PTreeOpt
import pandas as pd

file = 'results/fit-historical/snapshots-s1-fit-storage-rmse.pkl'
# file = 'results/opt-historical/snapshots-s3-obs-no_pulse.pkl'
snapshots = pickle.load(open(file, 'rb'), encoding='latin1')
P = snapshots['best_P'][-1]
# print(str(P))

# print out two tables, power and revenue
print('Power (GWh/year)')

vegscens = ['Control', 'Treatment',
            'OldFireModel_Extreme_Control',
            'OldFireModel_Moderate_Control',
            'OldFireModel_Extreme_Treatment',
            'OldFireModel_Moderate_Treatment']
            
cols_to_save = ['dowy', 'SFMD', 'RFMD', 'QFMD', 'SHHL', 'RHHL',
       'QHHL', 'total_power']

for vegscen in vegscens:
  for envscen in ['no_pulse', 'FERC', 'increase_rampdown', 'increase_rampdown_BN']:
    
    model = MFPModel('mfp/data/mfp_data.csv', 
                      sd='1980-10-01', ed='2015-09-30', # end date for Phil's data
                      env_scenario=envscen,
                      veg_scenario=vegscen,
                      fit_historical=True)

    df = model.f(P=P, mode='simulation')
    df[cols_to_save].to_csv('results/timeseries/hist-policy/%s_%s.csv' % (vegscen,envscen))

    power = df.total_power.resample('AS-OCT').sum().mean()/1000
    print('%0.2f ' % power, end='')
  print('')


# No revenue calculations if running back to 1980 (CAISO price data starts in 2009)

# print('\nRevenue ($M/year)')

# for vegscen in ['Control', 'Treatment', 'eelt_75', 'eeln_75']:
#   for envscen in ['no_pulse', 'FERC', 'increase_rampdown', 'increase_rampdown_BN']:
#     model = MFPModel('mfp/data/mfp_data.csv', 
#                       sd='1980-10-01', ed='2015-09-30', # end date for Phil's data
#                       env_scenario=envscen,
#                       veg_scenario=vegscen,
#                       fit_historical=True)

#     df = model.f(P=P, mode='simulation')
#     rev = df.total_revenue.resample('A').sum().mean()/1000000

#     print('%0.2f ' % rev, end='')

#   print('')
