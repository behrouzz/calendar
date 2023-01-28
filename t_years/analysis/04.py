import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels import api as sm
import pickle

df = pd.read_csv('full.csv')

year = df['date'].str[:-6].astype(int).values

df['greg_year'] = df['date'].str[:-6].astype(int)

df.loc[df['greg_year']<0, 'greg_year'] = \
            df.loc[df['greg_year']<0, 'greg_year'] + 1

df['greg_month'] = df['date'].str[-5:-3].astype(int)
df['greg_day'] = df['date'].str[-2:].astype(int)

df['pers_year'] = df['greg_year'] - 621

new_df = df[['et', 'time', 'greg_year', 'greg_month', 'greg_day', 'pers_year']]

with open('equinox_time.pickle', 'wb') as f:
    pickle.dump(new_df, f)


"""
df['pers_year'] = np.nan

c1 = df['greg_year']>621
df.loc[c1, 'pers_year'] = df.loc[c1, 'greg_year'] - 621

c2 = (df['greg_year']>=1) & (df['greg_year']<=621)
df.loc[c2, 'pers_year'] = df.loc[c2, 'greg_year'] - 622

c3 = df['greg_year']<1
df.loc[c3, 'pers_year'] = df.loc[c3, 'greg_year'] - 621

df['pers_year'] = df['pers_year'].astype(int)
"""



#import calendar
#calendar.isleap(2022)

##Zero and negative years are interpreted as prescribed by the ISO 8601 standard.
##Year 0 is 1 BC, year -1 is 2 BC, and so on.

