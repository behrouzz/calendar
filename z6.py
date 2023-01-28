from percal.birashk import *
import pickle
import numpy as np


date0 = (-50000, 1, 1)
jd0 = -16314154.5

y1 = -50000
y2 = 50000

leaps = leaps_between_two_years(y1, y2+1)

years = np.arange(y1+1, y2+1)
"""
ls = []
for y in years:
    date = (y, 1, 1)
    n = 366 if y in leaps else 365
    jd = jd0 + n
    ls.append(jd)
    jd0 = jd


years = [y1] + list(years)
jds = [-16314154.5] + ls

dc = {k:v for (k,v) in zip(years,jds)}

with open('all_years_1farvardin_jds.pickle', 'wb') as f:
    pickle.dump(dc, f)
"""

with open('all_years_1farvardin_jds.pickle', 'rb') as f:
    dc = pickle.load(f)

new_dc = {}
for k,v in dc.items():
    if k%1000==0:
        new_dc[k]=v
