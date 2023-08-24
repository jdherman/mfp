import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# cfs_taf = 2.29568411*10**-5 * 86400 / 1000
# taf_cfs = 1000 / 86400 * 43560

df = pd.read_csv('mfp/data/mfp_data.csv', index_col=0, parse_dates=True)
df['FMD_out'] = (df.FMD_out_FMPH + df.FMD_out_MF)#/400
df['HHL_out'] = (df.HHL_out_RR + df.HHL_out_MFPH)#/920

df[['FMD_out', 'HHL_out']].plot(kind='scatter', x='FMD_out', y='HHL_out')
print(np.corrcoef(df['FMD_out'].values, df['HHL_out'].values))
plt.show()

# df[['RFMD','RHHL']] *= taf_cfs




# plt.show()
