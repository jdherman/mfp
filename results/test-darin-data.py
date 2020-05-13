import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# should match columns
vegscens = ['Control', 'Treatment',
            'OldFireModel_Extreme_Control',
            'OldFireModel_Moderate_Control',
            'OldFireModel_Extreme_Treatment',
            'OldFireModel_Moderate_Treatment']

envscen = 'FERC'

historopt = 'hist'

# comparison 1: total power generation FRM+HHL
df_FRM = pd.read_csv('oasis-csv/FRM-monthly-generation-MWh.csv', index_col=0, parse_dates=True)
df_HHL = pd.read_csv('oasis-csv/HHL-monthly-generation-MWh.csv', index_col=0, parse_dates=True)

print('Comparing total annual generation...')
for vs in vegscens:
  fname = vs + '_' + envscen + '.csv'
  df = pd.read_csv('timeseries/%s-policy/'%historopt + fname, index_col=0, parse_dates=True)
  power = df.total_power.resample('AS-OCT').sum() / 1000
  power2 = (df_FRM[vs] + df_HHL[vs]).resample('AS-OCT').sum() / 1000
  r2 = np.corrcoef(power.values, power2.values)**2
  print(fname + ',' + str(r2[0,1]))

  power.plot()
  power2.plot()
  plt.legend(['Simplified Model', 'Full Operational Model'])
  plt.ylabel('FRM+HHL total generation, GWh/year')
  plt.savefig('oasis-plots/%s-policy/'%historopt + 'total-power_%s_%s.svg' % (vs, envscen))
  plt.close()

# comparison 2: storage at different timescales
print('Comparing HHL daily storage...')
df_FRM = pd.read_csv('oasis-csv/FRM-daily-storage-AF.csv', index_col=0, parse_dates=True)
df_HHL = pd.read_csv('oasis-csv/HHL-daily-storage-AF.csv', index_col=0, parse_dates=True)

for vs in vegscens:
  fname = vs + '_' + envscen + '.csv'
  df = pd.read_csv('timeseries/%s-policy/'%historopt + fname, index_col=0, parse_dates=True)
  storage = df.SHHL
  storage2 = df_HHL[vs] / 1000
  r2 = np.corrcoef(storage.values, storage2.values)**2
  print(fname + ',' + str(r2[0,1]))
  storage.plot()
  storage2.plot()
  plt.legend(['Simplified Model', 'Full Operational Model'])
  plt.ylabel('Storage (TAF)')
  plt.savefig('oasis-plots/%s-policy/'%historopt + 'HHLStorage_%s_%s.png' % (vs, envscen))
  plt.close()

print('Comparing FMD daily storage...')
for vs in vegscens:
  fname = vs + '_' + envscen + '.csv'
  df = pd.read_csv('timeseries/%s-policy/'%historopt + fname, index_col=0, parse_dates=True)
  storage = df.SFMD
  storage2 = df_FRM[vs] / 1000
  r2 = np.corrcoef(storage.values, storage2.values)**2
  print(fname + ',' + str(r2[0,1]))
  storage.plot()
  storage2.plot()
  plt.legend(['Simplified Model', 'Full Operational Model'])
  plt.ylabel('Storage (TAF)')
  plt.savefig('oasis-plots/%s-policy/'%historopt + 'FMDStorage_%s_%s.png' % (vs, envscen))
  plt.close()