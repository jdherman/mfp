from __future__ import division
import numpy as np 
import pandas as pd

cfs_taf = 2.29568411*10**-5 * 86400 / 1000
taf_cfs = 1000 / 86400 * 43560
cms_cfs = 35.3146667

class MFPModel():

  def __init__(self, datafile, sd, ed,
               fit_historical = False, use_tocs = False, 
               cc = False, scenario = None, multiobj = False,
               env_scenario = 'no_pulse', veg_scenario = 'obs'):

    self.df = pd.read_csv(datafile, index_col=0, parse_dates=True)[sd:ed]
    self.multiobj = multiobj

    self.T = len(self.df.index)
    self.fit_historical = fit_historical

    dfenv = pd.read_csv('mfp/data/env-flow-scenarios.csv', index_col=0, parse_dates=True)[sd:ed]
    self.envFMD = dfenv['FMD_%s' % env_scenario].values
    self.envHHL = dfenv['HHL_%s' % env_scenario].values

    if veg_scenario != 'obs':
      dfveg = pd.read_csv('mfp/data/phil-frm-veg-scenarios.csv', 
                          index_col=0, parse_dates=True)[sd:ed]

      self.vegQ = (dfveg[veg_scenario] * cms_cfs * dfveg['bias_cor']).values 
      self.veg = True
    else:
      self.veg = False

    # we assume the two operations are perfectly correlated
    # historically this is close but not quite true
    # print self.df[['FMD_out_FMPH','HHL_out_MFPH']].corr() # 0.64
    # print self.df[['FMD_storage','HHL_storage']].corr() # 0.90
    
  def f(self, P=None, mode='optimization'):

    T = self.T
    SFMD,RFMD,SHHL,RHHL,total_power,total_revenue = [np.zeros(T) for _ in range(6)]
    
    KF = 134 # capacity, TAF (changed from 134 to match observed -- maybe dead pool?)
    KH = 208 # capacity, TAF
    # reselevF = 5244.5 # reservoir elevation, ft
    # reselevH = 4630 # reservoir elevation, ft
    elevFMPH = 4630 # powerhouse elevation, ft
    elevMFPH = 2529 # powerhouse elevation, ft
    maxflowFMPH = 400 # max powerhouse flow, cfs
    maxflowMFPH = 920 # max powerhouse flow, cfs

    # storage-elevation curves (assume linear)
    # https://waterdata.usgs.gov/ca/nwis/wys_rpt/?site_no=11428700
    # https://waterdata.usgs.gov/ca/nwis/wys_rpt/?site_no=11427400
    # returns water elevation estimates in ft. ASL
    FMDmin = 40 # TAF, deadpool? (from historical data)
    HHLmin = 50 # same deal
    SE_FMD = lambda x: (x-FMDmin)*(5244-5125)/(KF-FMDmin) + 5125
    SE_HHL = lambda x: (x-HHLmin)*(4630-4288)/(KH-HHLmin) + 4288

    dowy = self.df.dowy

    if not self.veg:
      QFMD = ((self.df.FMD_in_duncan + self.df.FMD_in_MF)
              .fillna(method='ffill').values * cfs_taf)
    else:
      QFMD = (self.vegQ + self.df.FMD_in_duncan.fillna(method='ffill').values) * cfs_taf

    QHHL = self.df.HHL_in_RR.fillna(method='ffill').values * cfs_taf

    RFMD[0] = (self.df.FMD_out_MF.ix[0] + self.df.FMD_out_FMPH.ix[0]) * cfs_taf
    SFMD[0] = self.df.FMD_storage.values[0]
    RHHL[0] = (self.df.HHL_out_RR.ix[0] + self.df.HHL_out_MFPH.ix[0]) * cfs_taf
    SHHL[0] = self.df.HHL_storage.values[0]

    policies = [None]

    for t in range(1,T):

      if P:
        policy,rules = P.evaluate([SFMD[t-1]+SHHL[t-1], dowy[t], QFMD[t]+QHHL[t]])
        # policy is a value on [0,1]
        # one policy, then disaggregate based on ratio of turbine capacity
        # (or ratio of current storage?)

        # set target release
        targetF = policy * maxflowFMPH * cfs_taf
        targetH = policy * maxflowMFPH * cfs_taf
      else:
        # from USGS:
        targetF = self.df.FMD_out_FMPH.ix[t] * cfs_taf
        targetH = self.df.HHL_out_MFPH.ix[t] * cfs_taf

      RFMD[t] = targetF
      RHHL[t] = targetH

      reselevF = SE_FMD(SFMD[t-1])
      reselevH = SE_HHL(SHHL[t-1])

      # env flows
      # Actual USGS releases:
      # envF = self.df.FMD_out_MF.ix[t] * cfs_taf
      # envH = self.df.HHL_out_RR.ix[t] * cfs_taf
      envF = self.envFMD[t] * cfs_taf 
      envH = self.envHHL[t] * cfs_taf

      # crop the values here (for both FMD and HHL)
      RFMD[t] = max(min(targetF, SFMD[t-1] - FMDmin + QFMD[t] - envF), 0)
      RFMD[t] = min(RFMD[t], maxflowFMPH * cfs_taf) # no floods included yet
      envF +=  max(SFMD[t-1] + QFMD[t] - RFMD[t] - envF - KF, 0) # spill, assume to env.

      RHHL[t] = max(min(targetH, SHHL[t-1] - HHLmin + QHHL[t] - envH), 0)
      RHHL[t] = min(RHHL[t], maxflowMFPH * cfs_taf) # no floods included yet
      envH +=  max(SHHL[t-1] + QHHL[t] - RHHL[t] - envH - KH, 0) # spill, assume to env.

      SFMD[t] = max(SFMD[t-1] + QFMD[t] - RFMD[t] - envF, FMDmin)
      SHHL[t] = max(SHHL[t-1] + QHHL[t] - RHHL[t] - envH + RFMD[t], HHLmin)

      # power generation, MWh/day
      power_FMPH = (24*0.80*10**-4/1.181)*(reselevF - elevFMPH)*RFMD[t]*taf_cfs
      power_MFPH = (24*0.80*10**-4/1.181)*(reselevH - elevMFPH)*RHHL[t]*taf_cfs
      total_power[t] = power_FMPH + power_MFPH
      # total_revenue[t] = total_power[t] * self.df.CAISO_LMP.ix[t]

    if mode == 'simulation' or self.multiobj:
      df = self.df.copy()
      df['SFMD'] = pd.Series(SFMD, index=df.index)
      df['RFMD'] = pd.Series(RFMD, index=df.index)
      df['QFMD'] = pd.Series(QFMD, index=df.index)
      df['SHHL'] = pd.Series(SHHL, index=df.index)
      df['RHHL'] = pd.Series(RHHL, index=df.index)
      df['QHHL'] = pd.Series(QHHL, index=df.index)
      df['total_power'] = pd.Series(total_power, index=df.index)
      # df['total_revenue'] = pd.Series(total_revenue, index=df.index)
      # df['demand'] = pd.Series(D, index=df.index)
      # df['target'] = pd.Series(target, index=df.index)


    if mode == 'simulation':
      # df['policy'] = pd.Series(policies, index=df.index, dtype='category')
      return df    
    else:
      if self.fit_historical:
        temp = pd.DataFrame(index=self.df.index)

        # to compare storage...
        # temp['obs'] = self.df.FMD_storage + self.df.HHL_storage
        # temp['sim'] = SFMD+SHHL

        # or to compare release... (harder to do)
        # temp['obs'] = self.df.FMD_out_FMPH + self.df.HHL_out_MFPH
        # temp['sim'] = RFMD+RHHL
        # temp = temp.resample('W').sum()
  
        # return -temp.corr().values[0,1]**2 # or use RMSE instead:

        # storage RMSE
        RMSE = (((self.df.FMD_storage - SFMD) ** 2).mean() ** .5
              + ((self.df.HHL_storage - SHHL) ** 2).mean() ** .5)
        # release RMSE
        # RMSE = (((self.df.FMD_out_FMPH - RFMD) ** 2).mean() ** .5
        #       + ((self.df.HHL_out_MFPH - RHHL) ** 2).mean() ** .5)

        # penalize anything below observed carryover
        ix = (self.df.index.month==9) & (self.df.index.day==30)
        a = self.df.FMD_storage[ix]
        b = pd.Series(SFMD, index=self.df.index)[ix]
        c = self.df.HHL_storage[ix]
        d = pd.Series(SHHL, index=self.df.index)[ix]

        if((b < a).any() or (d < c).any()):
          return 10**10 # arbitrary large number
        else:
          return RMSE
        
      else:
        # objective: average annual revenue ($M)
        # or average annual generation (GWh)
        # rev = (pd.Series(total_revenue, index=self.df.index)
        #        .resample('AS-OCT').sum().mean()/1000000)
        power = (pd.Series(total_power, index=self.df.index)
                 .resample('AS-OCT').sum().mean()/1000)

        # enforce carryover values from historical
        # penalize anything below the observed carryover storage
        ix = (self.df.index.month==9) & (self.df.index.day==30)
        a = self.df.FMD_storage[ix]
        b = pd.Series(SFMD, index=self.df.index)[ix]
        c = self.df.HHL_storage[ix]
        d = pd.Series(SHHL, index=self.df.index)[ix]

        if((b < a).any() or (d < c).any()):
          return 0
        else:
          return -power
        # if not self.multiobj:
        #   return shortage_cost.sum() + flood_cost.sum() # + EOP
          # instead return total hydropower generation

        # else:
        #   J1 = shortage_cost.sum() # water supply
        #   J2 = taf_to_cfs(df.Rs.max()) # peak flood
        #   # (3) environmental alteration:
        #   # integrate between inflow/outflow exceedance curves
        #   ixi = np.argsort(Q)
        #   ixo = np.argsort(R)
        #   J3 = np.trapz(np.abs(Q[ixi]-R[ixo]), dx=1.0/T)
        #   # (4) Maximize hydropower generation (GWh)
        #   J4 = -df.power.resample('AS-OCT').sum().mean() / 1000 
        #   return [J1,J2,J3,J4]


