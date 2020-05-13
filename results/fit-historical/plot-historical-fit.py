from __future__ import division
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
from mfp import MFPModel
import pickle

sns.set_style('whitegrid')

cfs_taf = 2.29568411*10**-5 * 86400 / 1000
taf_cfs = 1000 / 86400 * 43560

# 8/22/17: found that seed 2 is the best (RMSE = 25ish)
# (FOR THE 2009-2016 period)

# 11/10/17: best seed is 1 (RMSE=35.11)
# (FOR THE 1980-2015 period)

# 11/14/17: best seed 4 (RMSE=43.2322981746)
# with the carryover constraint applied

# for s in range(10):
#   snapshots = pickle.load(open('snapshots-s%d-fit-storage-rmse.pkl' % s, 'rb'), encoding='latin1')
#   if snapshots:
#     print(str(s) + ', ' + str(snapshots['best_f'][-1]))

snapshots = pickle.load(open('snapshots-s4-fit-storage-rmse.pkl', 'rb'), encoding='latin1')
P = snapshots['best_P'][-1]

model = MFPModel('mfp/data/mfp_data.csv', 
                  sd='1980-10-01', ed='2015-09-30',
                  env_scenario='no_pulse',
                  fit_historical=True)
df = model.f(P=P, mode='simulation')

# # print(df.total_power.resample('A').sum())

df[['RFMD','RHHL']] *= taf_cfs

# df[['SFMD','FMD_storage','SHHL','HHL_storage','RFMD','FMD_out_FMPH','RHHL','HHL_out_MFPH']].to_csv('data-for-phil.csv')

ax = plt.subplot(2,1,1)
df[['SFMD','FMD_storage']].plot(ax = ax)
plt.ylabel('FMD Storage (TAF)')
plt.legend(['Modeled', 'Observed'])
plt.ylim([0,150])

r2 = np.corrcoef(df.SFMD.values, df.FMD_storage.values)**2
print('FMD R2: %0.2f' % r2[0,1])

ax = plt.subplot(2,1,2)
df[['SHHL','HHL_storage']].plot(ax = ax)
plt.ylabel('HHL Storage (TAF)')
plt.legend(['Modeled', 'Observed'])
plt.ylim([0,220])

r2 = np.corrcoef(df.SHHL.values, df.HHL_storage.values)**2
print('HHL R2: %0.2f' % r2[0,1])

# df[['RFMD','FMD_out_FMPH']].plot()
# df[['RHHL','HHL_out_MFPH']].plot()
# plt.ylabel('HHL Storage (TAF)')

plt.show()
