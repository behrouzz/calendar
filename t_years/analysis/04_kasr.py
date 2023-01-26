import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels import api as sm


df = pd.read_csv('full.csv')

year = df['date'].str[:-6].astype(int).values
i_after2000 = np.where(year>=2000)[0]

dt = df['et'].diff().values/86400

df['kasr'] = dt - 365

##df['greg_year'] = df['date'].str[:-6].astype(int)
##df['pers_year'] = np.nan
##
##c1 = df['greg_year']>621
##df.loc[c1, 'pers_year'] = df.loc[c1, 'greg_year'] - 621
##
##c2 = (df['greg_year']>=1) & (df['greg_year']<=621)
##df.loc[c2, 'pers_year'] = df.loc[c2, 'greg_year'] - 622
##
##c3 = df['greg_year']<1
##df.loc[c3, 'pers_year'] = df.loc[c3, 'greg_year'] - 621
##
##df['pers_year'] = df['pers_year'].astype(int)

h = np.array([int(i.split(':')[0]) for i in df['time']])
m = np.array([int(i.split(':')[1]) for i in df['time']])
s = np.array([float(i.split(':')[2]) for i in df['time']])

df['t'] = h + (m/60) + (s/3600)
df['kt'] = df['t']/24

df['leap'] = False

df.loc[df['kt']<df['kasr'].mean(), 'leap'] = True
#import calendar
#calendar.isleap(2022)

##Zero and negative years are interpreted as prescribed by the ISO 8601 standard.
##Year 0 is 1 BC, year -1 is 2 BC, and so on.

