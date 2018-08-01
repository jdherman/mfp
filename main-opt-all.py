import numpy as np
# import matplotlib.pyplot as plt
import pickle
from mfp import MFPModel
from ptreeopt import PTreeOpt
import pandas as pd
import os

vegscens = ['Control', 'Treatment',
            'OldFireModel_Extreme_Control',
            'OldFireModel_Moderate_Control',
            'OldFireModel_Extreme_Treatment',
            'OldFireModel_Moderate_Treatment']

for vegscen in vegscens:
  for envscen in ['no_pulse', 'FERC', 'increase_rampdown', 'increase_rampdown_BN']:
    for seed in range(10):

      outfile = 'results/opt-historical-apr2018/snapshots-s%d-%s-%s.pkl' % (seed,vegscen,envscen)
      if os.path.isfile(outfile):
        continue

      np.random.seed(seed)

      model = MFPModel('mfp/data/mfp_data.csv', 
                        sd='1980-10-01', ed='2015-09-30', # end date for Phil's data
                        env_scenario=envscen,
                        veg_scenario=vegscen,
                        fit_historical=False)

      # all units in TAF or TAF/d (not going all the way to full cap)
      algorithm = PTreeOpt(model.f, 
                          feature_bounds = [[0,270], [1,365], [3,16]],
                          feature_names = ['Storage', 'Day', 'Inflow'],
                          discrete_actions = False,
                          action_bounds = [0,1], # pct of hydro capacity release
                          mu = 20,
                          cx_prob = 0.70,
                          population_size = 256,
                          max_depth = 10
                          )


      snapshots = algorithm.run(max_nfe = 200000, log_frequency = 2000, parallel=True)

      if snapshots: # ONLY MASTER saves results
        pickle.dump(snapshots, open(outfile, 'wb'))
