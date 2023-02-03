import spiceypy as sp
import numpy as np
from scipy import interpolate
from scipy.optimize import fsolve
from hypatie import car2sph
import pickle
from glob import glob
import pandas as pd


def dec_sun(et):
    # J2000
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sun_2000 = pos[:3] #GCRS
    _, dec_2000, _ = car2sph(sun_2000)
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    # equinox of date
    sun_date = np.matmul(rotmat, sun_2000)
    _, dec_date, _ = car2sph(sun_date)
    return dec_2000, dec_date


file = '../t_years/analysis/equinox_time.csv'
ET, TIME, GY, GM, GD, PY = pd.read_csv(file).iloc[5000]
JD = (ET/86400) + 2451545.0


sp.furnsh('C:/Moi/_py/Astronomy/Solar System/kernels/heavy.tm')

print(ET)
s = sp.etcal(ET)
print(s)
new_et = sp.str2et(s + ' UTC')
print(new_et)
new_s = sp.etcal(new_et)
print(new_s)

sp.kclear()

