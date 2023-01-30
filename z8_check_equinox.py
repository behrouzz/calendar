import spiceypy as sp
import numpy as np
from scipy import interpolate
from scipy.optimize import fsolve
from hypatie import car2sph
import pickle
from glob import glob
import pandas as pd


def true_sun(et):
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sunJ2000 = pos[:3] #GCRS
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec, r = car2sph(sun)
    return ra, dec


df = pd.read_csv('t_years/analysis/equinox_time.csv').sample(10)
#df['jd'] = (df['et']/86400) + 2451545.0

et0 = df['et'].iloc[0]

et1 = et0 - 10000
et2 = et0 + 10000


sp.furnsh('C:/Moi/_py/Astronomy/Solar System/kernels/heavy.tm')

#t_ver = []

ets = np.linspace(et1, et2, 100000)

dec = np.zeros((len(ets),))
for i, et in enumerate(ets):
    _, dec[i] = true_sun(et)

i_ver = np.argmin(np.abs(dec))

if np.abs(dec).min()>0.001: # check accuracy
    print('WARNING:', np.abs(dec).min())

##f = interpolate.interp1d(ets, dec, kind='cubic')
##root = fsolve(f, ets[i_ver])[0]

print(et0 - ets[i_ver])
##t_ver.append(root)
##
##
##t_ver = np.array(t_ver)

sp.kclear()
