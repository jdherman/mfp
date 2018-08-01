import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

def water_day(d):
  return d - 274 if d >= 274 else d + 91
water_year = lambda d: d.year+1 if d.dayofyear >= 274 else d.year

# just get the index from this
df = pd.read_csv('mfp_data.csv', parse_dates=True, index_col=0)['1980-10-01':]
# fill out this empty one
df = pd.DataFrame(index=df.index)

# add dowy and wyt first
df['dowy'] = pd.Series([water_day(d) for d in df.index.dayofyear], index=df.index)
df['WY'] = pd.Series([water_year(d) for d in df.index], index=df.index)
df['WYT'] = pd.Series()

# need Folsom full natural flows to find WYT
dfolsom = pd.read_csv('AMF-FNF.csv', index_col=0, parse_dates=True)
dfolsom = dfolsom.resample('AS-OCT').sum()/1000

for year in range(1981,2017):
  Q = dfolsom[str(year-1)].values[0][0]

  if Q > 3400:
    v = 'W'
  elif Q > 2400:
    v = 'AN'
  elif Q > 1500:
    v = 'BN'
  elif Q > 1000:
    v = 'D'
  elif Q > 600:
    v = 'C'
  else:
    v = 'EC'

  # print(year, ': ', v)

  df.loc[df.WY==year, 'WYT'] = v


df.loc['2016-09-30', 'WYT'] = 'AN' # hack

# no-pulse year round instream flow reqs (from Kristen), monthly cfs
instream = { 
  'FMD': {
    'W': [13,13,14.5,20,20,17,13,13,13,13,13,13],
    'AN': [11,11,13,20,20,16,11,11,11,11,11,11],
    'BN': [10,10,10.5,13,13,12,10,10,10,10,10,10],
    'D': [9,9,10,13,13,11,9,9,9,9,9,9],
    'C': [8,8,9.5,11,11,8,8,8,8,8,8,8],
    'EC': [8,8,9.5,11,11,8,8,8,8,8,8,8]
  },
  'HHL': {
    'W': [25,25,40,60,60,45,30,30,30,25,25,25],
    'AN': [25,25,40,55,55,45,30,30,30,25,25,25],
    'BN': [20,20,30,42,42,25,20,20,20,20,20,20],
    'D': [20,20,27.5,35,35,24,20,20,20,20,20,20],
    'C': [15,15,22.5,31,23,17,15,15,15,15,15,15],
    'EC': [15,15,22.5,31,23,17,15,15,15,15,15,15]
  }
}

def get_instream(x, res):
  return instream[res][x.WYT][x.name.month-1]

for r in ['FMD','HHL']:
  s = '%s_no_pulse' % r
  df[s] = df.apply(get_instream, res=r, axis=1)
  # make other copies
  for scen in ['FERC', 'increase_rampdown', 'increase_rampdown_BN']:
    df['%s_%s' % (r,scen)] = df[s]

# now add in pulse flows
# this is hard to do without just hacking it together
# all data from Kristen's excel file
# May 15 - Jun 27 water days

pulse = {
  'FMD': {
    'FERC': [200,400,400,400,400,400,400,400,400,
             275,275,190,190,190,115,115,115,65,65,65,65],
    # 'increase': [220,440,440,440,440,440,440,440,440,
    #             440,302.5,302.5,302.5,209,209,209,209,
    #             126.5,126.5,126.5,126.5,71.5,71.5,71.5,71.5,71.5],
    'increase_rampdown': [220,440,440,440,440,440,440,440,440,
                          440,302.5,302.5,242,209,209,209,167.2,
                          122.76,126.5,126.5,101.2,80.96,71.5,71.5,71.5,71.5],
    'increase_rampdown_BN': [220,440,440,440,440,440,440,440,440,
                          440,302.5,302.5,242,209,209,209,167.2,
                          122.76,126.5,126.5,101.2,80.96,71.5,71.5,71.5,71.5]
  },
  'HHL': {
    'FERC': [200,200,200,200,200,200,200,200,
            200,200,200,200,200,200,200,200,
            200,200,200,200,200,200,200,200,
            200,200,200,200,200,200,200,200,
            200,200,200,150,150,90,90,90],
    # 'increase': [220,220,220,220,220,220,220,220,
    #             220,220,220,220,220,220,220,220,
    #             220,220,220,220,220,220,220,220,
    #             220,220,220,220,220,220,220,220,
    #             220,220,220,220,220,165,165,165,
    #             99,99,99,99],
    'increase_rampdown': [220,220,220,220,220,220,220,220,
                          220,220,220,220,220,220,220,220,
                          220,220,220,220,220,220,220,220,
                          220,220,220,220,220,220,220,220,
                          220,220,220,220,176,165,132,105.6,
                          99,99,99,99],
    'increase_rampdown_BN': [220,220,220,220,220,220,220,220,
                          220,220,220,220,220,220,220,220,
                          220,220,220,220,220,220,220,220,
                          220,220,220,220,220,220,220,220,
                          220,220,220,220,176,165,132,105.6,
                          99,99,99,99]
  }
}

dowy_start = 226 # may 15th
num_years = 7

for r in ['FMD','HHL']:
  # s = '%s_no_pulse' % r
  # df[s] = df.apply(get_instream, res=r, axis=1)
  # make other copies
  for scen in ['FERC', 'increase_rampdown']:
    data = pulse[r][scen]
    s = '%s_%s' % (r,scen)
    dowy_end = dowy_start + len(data)
    ix = (df.dowy >= dowy_start) & (df.dowy < dowy_end) & ((df.WYT == 'W') | (df.WYT == 'AN'))
    num_years = int(sum(ix)/len(data))
    df.loc[ix, s] = np.tile(data, num_years)

  for scen in ['increase_rampdown_BN']:
    data = pulse[r][scen]
    s = '%s_%s' % (r,scen)
    dowy_end = dowy_start + len(data)
    ix = (df.dowy >= dowy_start) & (df.dowy < dowy_end) & ((df.WYT == 'W') | (df.WYT == 'AN') | (df.WYT == 'BN'))
    num_years = int(sum(ix)/len(data))
    df.loc[ix, s] = np.tile(data, num_years)

df.plot()
plt.show()

df.to_csv('env-flow-scenarios.csv')




