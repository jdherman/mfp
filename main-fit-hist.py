import numpy as np
import matplotlib.pyplot as plt
import pickle
from mfp import MFPModel
from ptreeopt import PTreeOpt
import pandas as pd

for seed in range(10):

  np.random.seed(seed)

  model = MFPModel('mfp/data/mfp_data.csv', 
                    sd='1980-10-01', ed='2015-09-30',
                    env_scenario='no_pulse',
                    veg_scenario='obs',
                    fit_historical=True)

  # checking that simulation output makes sense...
  # df = model.f(mode='simulation')
  # df[['FMD_storage','SFMD']].plot()
  # df[['HHL_storage','SHHL']].plot()
  # print(df.total_power.resample('AS-OCT').sum())
  # plt.show()

  # all units in TAF or TAF/d (not going all the way to full cap)
  algorithm = PTreeOpt(model.f, 
                      feature_bounds = [[0,270], [1,365], [3,16]],
                      feature_names = ['Storage', 'Day', 'Inflow'],
                      discrete_actions = False,
                      action_bounds = [0,1], # pct of hydro capacity release
                      mu = 20,
                      cx_prob = 0.70,
                      population_size = 96,
                      max_depth = 10
                      )

  snapshots = algorithm.run(max_nfe = 200000, log_frequency = 2000, parallel=True)
  pickle.dump(snapshots, open('results/fit-historical/snapshots-s%d-fit-storage-rmse.pkl' % seed, 'wb'))
