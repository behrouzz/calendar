import numpy as np
import pickle

r2d = 180/np.pi

with open('vsop87d_earth_lon.pickle', 'rb') as f:
    data_arr = pickle.load(f)

# T = (JD-2451545)/365250
# JD should be in TT
# we know that: TT = TAI + 32.184
# we know that: TAI = UTC + LP

def earth_lon(T, data_arr):
    longitude = 0
    for alpha in range(6):
        arr = data_arr[data_arr[:,0]==alpha]
        A = arr[:,1]
        B = arr[:,2]
        C = arr[:,3]
        lon_part = 0
        for i in range(len(arr)):
            lon_part += T**alpha * A[i] * np.cos(B[i] + C[i]*T)
        longitude += lon_part
    return (longitude*r2d) % 360



#================================================
from datetime import datetime, timedelta
from hypatie.time import utc2tt, datetime_to_jd

utc = datetime(2023,3,1, 15,20)
tt = utc2tt(utc)
JD = datetime_to_jd(tt)
T = (JD-2451545)/365250

print(earth_lon(T, data_arr))

#=======================================================

from requests import request
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt


BASE_URL = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&'

FMT_BC = 'b%Y-%b-%d %H:%M:%S.%f'

t1 = '2023-03-01 15:20'
t2 = '2023-03-01 15:21'
steps = 5

script = f"""MAKE_EPHEM=YES
COMMAND=399
EPHEM_TYPE=OBSERVER
CENTER='500@10'
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
print(df)

