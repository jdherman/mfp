import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

cfs_taf = 2.29568411*10**-5 * 86400 / 1000
taf_cfs = 1000 / 86400 * 43560
cms_cfs = 35.3146667

sd = '1980-10-01'
ed = '2015-09-30'
df = pd.read_csv('mfp_data.csv', index_col=0, parse_dates=True)[sd:ed] * cfs_taf
dfveg = pd.read_csv('phil-frm-veg-scenarios.csv', 
                          index_col=0, parse_dates=True)[sd:ed] * cms_cfs * cfs_taf

# to figure out bias correction from Phil's data
print(dfveg.sum(axis=0))

print(df['FMD_in_MF'].sum(axis=0))
print(df['FMD_in_duncan'].sum(axis=0))

# df.CAISO_LMP.plot()
# plt.show()

# FM = df.FMD_out_FMPH.resample('M').mean()
# HH = df.HHL_out_MFPH.resample('M').mean()

# r = np.corrcoef(FM.values,HH.values)[0,1]
# plt.scatter(FM.values, HH.values, s=10, c='steelblue', edgecolor='none', alpha=0.7)
# plt.xlabel('FM Hydropower Release (cfs)')
# plt.ylabel('HH Hydropower Release (cfs)')
# plt.annotate('$R^2 = %f$' % r**2, xy=(0,800), color='0.3')

# plt.show()

# plt.ylabel('Release, CFS')
# plt.title('Hell Hole Outflow into Rubicon (Bypass Reach)')
# plt.show()


# df.FMD_storage.plot()
# plt.show()

# phil = pd.read_csv('phil-frm-veg-scenarios.csv', index_col=0, parse_dates=True)[sd:ed] * cms_cfs
# print(phil.columns)
# phil.plot(ax=ax)
# plt.show()
