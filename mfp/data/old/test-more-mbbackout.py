import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('usgs-hhtunnel.csv', index_col=0, parse_dates=True)
df.columns = ['hhtunnel']

df2 = pd.read_csv('usgs-duncan-before.csv', index_col=0, parse_dates=True)
df3 = pd.read_csv('usgs-duncan-after.csv', index_col=0, parse_dates=True)
df['duncan_div'] = pd.Series(df2.flow_cfs.values - df3.flow_cfs.values, index=df.index)

df2 = pd.read_csv('historical-storage.csv', index_col=0, parse_dates=True)
df['storage'] = pd.Series()
df.storage['2000-10-01':] = df2.storage[:'2015-09-30'].values

df2 = pd.read_csv('historical-outflow.csv', index_col=0, parse_dates=True)
df['outflow'] = pd.Series()
df.outflow['2000-10-01':'2015-09-30'] = df2.flow_cfs['2000-10-01':].values

df2 = pd.read_csv('frm-daily-inflow.csv', index_col=0, parse_dates=True)
df['inflow'] = pd.Series()
df.inflow['2000-10-01':] = df2.streamflow['2000-10-01':'2015-09-30'].values

df = df['2011-10-01':]

df[['hhtunnel', 'duncan_div', 'inflow', 'outflow']] *= 2.29568411*10**-5 * 86400

# df.storage.plot()

est_hhtunnel = df.storage.diff() - df.inflow - df.duncan_div + df.outflow

plt.scatter((-1*est_hhtunnel.values), df.hhtunnel.values)
# (-1*est_hhtunnel).plot()
# df.hhtunnel.plot()
# dS = (df.inflow + df.duncan_div - df.outflow - df.hhtunnel)
# (df.storage.iloc[0] + dS.cumsum()).plot()

plt.show()




# # df = pd.read_csv('frm-daily-inflow.csv', index_col=0, parse_dates=True)
# # df.streamflow.plot()

# plt.show()