import pandas as pd 
import matplotlib.pyplot as plt
from ulmo.usgs import nwis as ug
import time

# use ulmo library to download USGS streamflow data

t = pd.date_range(start='1980-10-01', end='2017-09-30')
df = pd.DataFrame(index=t)

sites = ['11427200', '11427500', '11427700', '11427750',
         '11427760', '11427960', '11428400', '11428600',
         '11428800', '11433060', '11433080']

# STREAMFLOW
for k in sites:
    print(k)
    data = ug.get_site_data(site_code=k, 
                            parameter_code='00060', 
                            service='dv', 
                            start='1980', end='2017')

    Q = pd.DataFrame(data['00060:00003']['values'])
    Q.index = pd.to_datetime(Q.datetime)
    df = pd.concat([df, Q.value.astype(float).rename('Q-'+k)], axis=1, copy=False)
    time.sleep(2)

sites = ['11427400','11428700']

# STORAGE
for k in sites:
    print(k)
    data = ug.get_site_data(site_code=k, 
                            parameter_code='00054', 
                            service='dv', 
                            start='1980', end='2017')

    Q = pd.DataFrame(data['00054:32400']['values'])
    Q.index = pd.to_datetime(Q.datetime)
    df = pd.concat([df, Q.value.astype(float).rename('S-'+k)], axis=1, copy=False)
    time.sleep(2)

df.to_csv('MFP_usgs.csv')
# df = pd.read_csv('MFP_storage_af.csv', index_col=0, parse_dates=True)
df.plot()
plt.show()
