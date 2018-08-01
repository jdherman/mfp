import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# df = pd.read_csv('usgs-hhtunnel.csv', index_col=0, parse_dates=True)

df = pd.read_csv('usgs-duncan-before.csv', index_col=0, parse_dates=True)
df2 = pd.read_csv('usgs-duncan-after.csv', index_col=0, parse_dates=True)

df['downstream'] = pd.Series(df2.flow_cfs.values, index=df.index)
(df.flow_cfs - df.downstream).plot()

# df = pd.read_csv('frm-daily-inflow.csv', index_col=0, parse_dates=True)
# df.streamflow.plot()

plt.show()