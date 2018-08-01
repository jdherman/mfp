import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('whitegrid')

df = pd.read_csv('frm-daily-inflow.csv', index_col=0, parse_dates=True)

water_supply = (df*2.29568411*10**-5*86400).resample('AS-OCT').sum().mean()
peak = df.resample('AS-OCT').max().mean()

fig,ax = plt.subplots()
ax.scatter(water_supply, peak, s=50)
ax.set_xlabel('Avg Annual Inflow (AF)')
ax.set_ylabel('Avg Annual Peak Flow (cfs)')

for i in range(4):
  ax.annotate(peak.index.values[i], (water_supply.values[i], peak.values[i]))

plt.show()