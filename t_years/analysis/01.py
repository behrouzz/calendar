import spiceypy as sp
import numpy as np
from glob import glob
import pickle
import matplotlib.pyplot as plt
import pandas as pd

ET0 = 6809763.812612681


sp.furnsh('../kernels/k_1600_2600.tm')
#===========================================

files = glob('../data/*')

around_2000 = [i for i in files if float(i.split('\\')[-1].split('_')[0])==ET0]
before_2000 = [i for i in files if float(i.split('\\')[-1].split('_')[0])<ET0]
after_2000  = [i for i in files if float(i.split('\\')[-1].split('_')[0])>ET0]

# Before 2000
# -----------
ls = []
for file in before_2000:
    with open(file, 'rb') as f:
        arr = pickle.load(f)
    ls.append(arr)
arr_before = np.sort(np.array([i for sublist in ls for i in sublist]))

# After 2000
# ----------
ls = []
for file in after_2000:
    with open(file, 'rb') as f:
        arr = pickle.load(f)
    ls.append(arr)
arr_after = np.sort(np.array([i for sublist in ls for i in sublist]))

# Around 2000
# -----------
for i in around_2000:
    if float(i.split('\\')[-1].split('_')[1])<ET0:
        with open(i, 'rb') as f:
            just_before = np.sort(pickle.load(f))
    elif float(i.split('\\')[-1].split('_')[1])>ET0:
        with open(i, 'rb') as f:
            just_after = np.sort(pickle.load(f))[1:]

# full
# ----

arr = np.append(arr_before, just_before)
arr = np.append(arr, just_after)
arr = np.append(arr, arr_after)

dt = (arr_after[1:] - arr_after[:-1])

print((dt/86400).min())
print((dt/86400).max())

with open('ets.pickle', 'wb') as f:
    pickle.dump(arr, f)

cal = sp.etcal(arr)
ets = [str(i) for i in arr]
df = pd.DataFrame({'et':ets, 'cal':cal})
df.set_index('et').to_csv('ets_cal.csv')


#===========================================
sp.kclear()
