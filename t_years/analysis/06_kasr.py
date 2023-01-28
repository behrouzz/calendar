import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels import api as sm


df = pd.read_csv('full.csv')

year = df['date'].str[:-6].astype(int).values
dt = df['et'].diff().values/86400
df['kasr'] = dt - 365

h = np.array([int(i.split(':')[0]) for i in df['time']])
m = np.array([int(i.split(':')[1]) for i in df['time']])
s = np.array([float(i.split(':')[2]) for i in df['time']])

df['t'] = h + (m/60) + (s/3600)
df['kt'] = df['t']/24


x = np.linspace(df['kasr'].mean()-0.05, df['kasr'].mean()+0.05, 10000)

arr = np.zeros((len(x),))

for i, val in enumerate(x):
    a = df.copy()
    a['leap'] = False
    a.loc[df['kt']<val, 'leap'] = True
    arr[i] = df['kasr'].sum() - a['leap'].sum()

ind = np.argmin(np.abs(arr))
print(x[ind])

df['leap'] = False
df.loc[df['kt']<x[ind], 'leap'] = True
