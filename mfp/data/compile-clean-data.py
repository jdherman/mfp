from __future__ import division
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

afd_cfs = 1 / 86400 * 43560

def water_day(d):
  return d - 274 if d >= 274 else d + 91

df = pd.read_csv('MFP_usgs.csv', index_col=0, parse_dates=True)
df['dowy'] = pd.Series([water_day(d) for d in df.index.dayofyear], index=df.index)

df[df < 0] = 0.0

# notes from Darin
c = {'S-11427400': 'FMD_storage', 
     'Q-11427200': 'FMD_out_FMPH',
     'Q-11427500': 'FMD_out_MF',
     'S-11428700': 'HHL_storage',
     'Q-11428800': 'HHL_out_RR'}

df.rename(columns=c, inplace=True)

df['FMD_in_duncan'] = df['Q-11427700'] - df['Q-11427750']
df.FMD_in_duncan[df.FMD_in_duncan < 0] = 0

df['FMD_in_MF'] = (df['FMD_storage'].diff()*afd_cfs
                 - df['FMD_in_duncan']
                 + df['FMD_out_FMPH']
                 + df['FMD_out_MF'])

df.loc[df.FMD_in_MF < 0, 'FMD_in_MF'] = 0

df['HHL_out_MFPH'] = (df['Q-11428600']
                    - df['Q-11433060']
                    - df['Q-11433080'])

df['HHL_in_RR'] = (df['HHL_storage'].diff()*afd_cfs
              - df['FMD_out_FMPH']
              + df['HHL_out_MFPH']
              + df['HHL_out_RR'])

# df['TOT_PH'] = df[['FMD_out_FMPH', 'HHL_out_MFPH']].sum(axis=1)
df.FMD_storage /= 1000
df.HHL_storage /= 1000


caiso = pd.read_csv('CAISO-LMP.csv', index_col=0, parse_dates=True)['10-01-2009':]
df['CAISO_LMP'] = caiso.lmp

# df.plot(kind='scatter', x='CAISO_LMP', y='TOT_PH')

# drop all the original USGS
df = df.loc[:, ~df.columns.str.contains('Q-|S-')]
df.fillna(method='ffill', inplace=True)
df[:'2016-09-30'].to_csv('mfp_data.csv')

# df = df.resample('M').mean()
# sns.lmplot('dowy', 'TOT_PH', hue='FMD_in_MF', data=df, fit_reg=False)

# df.filter(like='S-').plot(kind='area')
# df[['FMD_in_duncan','FMD_in_MF']].plot(kind='area')
# df[['Q-11427500','Q-11427200']].plot(kind='area')
# df[['Q-11428800', 'HHL_out_MFPP']].plot(kind='area')
# df['Q-11427200'].plot()
# df.HHL_in.plot()
# plt.show()
