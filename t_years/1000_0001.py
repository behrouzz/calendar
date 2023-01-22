import spiceypy as sp
import numpy as np
from scipy import interpolate
from scipy.optimize import fsolve
from hypatie import car2sph
import pickle


def true_sun(et):
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sunJ2000 = pos[:3] #GCRS
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec, r = car2sph(sun)
    return ra, dec


sp.furnsh('kernels/k_13202BC_1600.tm')
#=====================================================

fin = sp.str2et('1 A.D. JAN 01 00:00:00 TDT') # calculate until this time
#print(sp.etcal(fin))

with open('data/-12679080487.02055_-31581684211.247944','rb') as f:
    y_ini, y_fin = pickle.load(f)[-2:]


t_ver = []
while y_fin > fin:
    len_year = y_ini - y_fin

    t1 = y_fin - len_year - 10000
    t2 = y_fin - len_year + 10000

    ets = np.linspace(t1, t2, 10000)

    dec = np.zeros((len(ets),))
    for i, et in enumerate(ets):
        _, dec[i] = true_sun(et)

    i_ver = np.argmin(np.abs(dec))

    if np.abs(dec).min()>0.001: # check accuracy
        print('WARNING:', np.abs(dec).min())

    f = interpolate.interp1d(ets, dec, kind='cubic')
    root = fsolve(f, ets[i_ver])[0]
    t_ver.append(root)

    y_ini = y_fin
    y_fin = root

t_ver = np.array(t_ver)

#=====================================================
sp.kclear()


with open(f"data/{t_ver[0]}_{t_ver[-1]}", 'wb') as f:
    pickle.dump(t_ver, f)



