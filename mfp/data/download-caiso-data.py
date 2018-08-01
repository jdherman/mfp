import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from pyiso import client_factory

# watch errors about XML parsing
caiso = client_factory('CAISO', timeout_seconds=180)
# dates = pd.date_range('10-01-2009', '09-30-2016', freq='D')
# df = pd.DataFrame(index=dates)
# df['lmp'] = pd.Series()

# after the first time, with some errors stopping it
dates = pd.date_range('09-11-2013', '09-30-2016', freq='D')
df = pd.read_csv('CAISO-LMP.csv', index_col=0, parse_dates=True)

for i in range(len(dates)-1):
# data = caiso.get_lmp(latest=True, node_id='MIDLFORK_2_B1', freq='D')
  data = caiso.get_lmp(start_at=dates[i], end_at=dates[i+1], node_id='MIDLFORK_2_B1')
  lmp = pd.DataFrame(data).set_index('timestamp').lmp.mean()
  df.lmp[dates[i]] = lmp
  print dates[i]

  if (i % 30 == 0): # save every so often
    df.to_csv('CAISO-LMP2.csv')

# and again at the end
df.to_csv('CAISO-LMP2.csv')
df.plot()
plt.show()
