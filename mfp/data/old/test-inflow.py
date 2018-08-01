import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('whitegrid')

def cfs_to_af(Q):
  return Q * 2.29568411*10**-5 * 86400


df = pd.read_csv('frm-daily-inflow.csv', index_col=0, parse_dates=True)

df2 = pd.read_csv('historical-outflow.csv', index_col=0, parse_dates=True)
df2 = df2['1980-01-01':]

df['historical_outflow'] = pd.Series()
df.historical_outflow['1980-01-01':'2015-09-30'] = df2.flow_cfs.values

df2 = pd.read_csv('historical-storage.csv', index_col=0, parse_dates=True)
df['historical_storage'] = pd.Series()
df.historical_storage['2000-10-01':] = df2.storage[:'2015-12-30'].values

df = df['2000-10-01':]
df.historical_storage.plot()
plt.ylabel('Storage (AF)')

df.streamflow = cfs_to_af(df.streamflow)
df.historical_outflow = cfs_to_af(df.historical_outflow)
dS =  (df.streamflow - df.historical_outflow)
est_outflow = df.historical_storage.diff() - df.streamflow
# dS += extra_outflow

# (df.historical_storage.iloc[0] + dS.cumsum()).plot()
# est_outflow.plot()
plt.show()

# Q = np.sort(df.historical_outflow.values)[::-1]
# plt.plot(Q)
# Q = np.sort(df.streamflow.values)[::-1]
# plt.plot(Q)
# plt.gca().set_yscale('log')
# plt.ylabel('Flow (cfs)')
# plt.legend(['Outflow (observed)', 'Inflow (from Phil)'])
# plt.show()