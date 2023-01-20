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

from datetime import datetime
from hypatie.time import utc2tt, datetime_to_jd

utc = datetime(2023,3,1, 15,20)
tt = utc2tt(utc)
JD = datetime_to_jd(tt)
T = (JD-2451545)/365250

print(earth_lon(T, data_arr))
