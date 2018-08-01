import numpy as np
import pickle
import pandas as pd

# should be NO empty files
vegscens = ['Control', 'Treatment',
            'OldFireModel_Extreme_Control',
            'OldFireModel_Moderate_Control',
            'OldFireModel_Extreme_Treatment',
            'OldFireModel_Moderate_Treatment']

for vegscen in vegscens:
  for envscen in ['no_pulse', 'FERC', 'increase_rampdown', 'increase_rampdown_BN']:

      print('\n%s,%s\n' % (vegscen,envscen))
      data = None
      
      for s in range(0,30):
        try:
          data = pickle.load(
            open('opt-historical/snapshots-s%d-%s-%s.pkl' % 
                  (s,vegscen,envscen), 'rb'), encoding='latin1') # encoding important py3
        except:
          continue
        
        if data:
          nfe = data['nfe']
          best_f = np.array(data['best_f'])
          print('%s, %0.2f, %s' % (s, -1*best_f[-1], data['best_P'][-1])) # to see tree logic

        # results = model.f(data['best_P'][-1])
        # print results
