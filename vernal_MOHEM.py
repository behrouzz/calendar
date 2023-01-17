# when ObsEcLon reaches 360 = vernal equinox

from datetime import datetime, timedelta
from requests import request
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt


BASE_URL = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&'

FMT_BC = 'b%Y-%b-%d %H:%M:%S.%f'

t1 = 'B.C. 2000-02-01 00:00'
t2 = 'B.C. 2000-10-31 00:00'
steps = 10000

script = f"""MAKE_EPHEM=YES
COMMAND=10
EPHEM_TYPE=OBSERVER
CENTER='500@399'
START_TIME='{t1}'
STOP_TIME='{t2}'
STEP_SIZE='{steps}'
QUANTITIES='1,31'
REF_SYSTEM='ICRF'
CAL_FORMAT='CAL'
TIME_DIGITS='SECONDS'
ANG_FORMAT='DEG'
APPARENT='AIRLESS'
RANGE_UNITS='KM'
SUPPRESS_RANGE_RATE='NO'
SKIP_DAYLT='NO'
SOLAR_ELONG='0,180'
EXTRA_PREC='NO'
RTS_ONLY='NO'
CSV_FORMAT='YES'
OBJ_DATA='NO'"""


script = script.replace('+','%2B').replace(' ', '%20')
url = BASE_URL + script
error_msg = ''
req = request('GET', url)
all_text = req.content.decode('utf-8')


if ('$$SOE' not in all_text) or ('$$EOE' not in all_text):
    error_msg = all_text[:all_text.find('$$SOF')]
    print(error_msg)
mark1 = all_text.find('$$SOE')
text = all_text[mark1+6:]
mark2 = text.find('$$EOE')
text = text[:mark2]
raw_rows = text.split('\n')[:-1]
raw_rows = [i.split(',')[:-1] for i in raw_rows]
rows = []
for r in raw_rows:
    row = [i.strip() for i in r if len(i.strip())>0]
    rows.append(row)

cols = ['ut_str','ra','dec','ObsEcLon','ObsEcLat']

df = pd.DataFrame(data=rows, columns=cols)

df['t'] = df['ut_str'].apply(lambda x: datetime.strptime(x, FMT_BC))
df['sec'] = (df['t'] - df['t'].iloc[0]).dt.total_seconds()

df[['ra', 'dec', 'ObsEcLon', 'ObsEcLat']] = \
    df[['ra', 'dec', 'ObsEcLon', 'ObsEcLat']].astype(float)

ind = df[df['ObsEcLon']==df['ObsEcLon'].max()].index[0]

df['LON'] = np.nan
df.iloc[:ind+1]['LON'] = df.iloc[:ind+1]['ObsEcLon']
df.iloc[ind+1:]['LON'] = df.iloc[ind+1:]['ObsEcLon'] + 360

f = interpolate.interp1d(df['sec'].values, df['LON'].values, kind='cubic')

t1 = df['sec'].iloc[ind]
t2 = df['sec'].iloc[ind+1]

x = np.linspace(t1, t2, 10000)
y = f(x)

equ_sec = x[np.argmin(np.abs(360-y))]
exact_t = timedelta(seconds=equ_sec) + df['t'].iloc[0]

print(exact_t) # vernal equinox
