import numpy as np
import pickle
import pandas as pd

# should be NO empty files

for vegscen in ['Control', 'Treatment', 'eelt_75', 'eeln_75']:
  for envscen in ['no_pulse', 'FERC', 'increase_rampdown']:

      # print('\n%s,%s' % (vegscen,envscen))

      bestf = 0.0
      bestP = None
      bestS = -1

      for s in range(30): # seeds 20-30 only exist for a few re-runs
        try:
          data = pickle.load(
            open('opt-historical-dec2017/snapshots-s%d-%s-%s.pkl' % 
                  (s,vegscen,envscen), 'rb'), encoding='latin1') # encoding important py3

          best_f = np.array(data['best_f'])

          if best_f[-1] < bestf:
            bestf = best_f[-1]
            bestP = data['best_P'][-1]
            bestS = s
        except:
          pass

      print('\'%s,%s\': %d, %0.2f' % (vegscen,envscen,bestS,bestf))
      # print('%0.2f' % (-1*bestf), end=' ') # to see tree logic
      if envscen is not 'no_pulse':
        bestP.graphviz_export('tree_pngs/Ptree-%s-%s.png' % (vegscen,envscen))
  # print('')
