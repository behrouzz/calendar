import spiceypy as sp
import numpy as np
from scipy import interpolate
from scipy.optimize import fsolve
from hypatie import car2sph
import pickle
from glob import glob


def true_sun(et):
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sunJ2000 = pos[:3] #GCRS
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec, r = car2sph(sun)
    return ra, dec


sp.furnsh('kernels/k_2600_17190.tm')
#=====================================================

fin = sp.str2et('9000 A.D. JAN 01 00:00:00 TDT') # calculate until this time
print(sp.etcal(fin))

files = glob('data/*')
et1 = max([float(i.split('_')[0].split('\\')[-1]) for i in files])
et2 = max([float(i.split('_')[-1]) for i in files])

with open(f'data/{et1}_{et2}','rb') as f:
    y_ini, y_fin = pickle.load(f)[-2:]


t_ver = []
while y_fin < fin:
    len_year = y_fin - y_ini

    t1 = y_fin + len_year - 10000
    t2 = y_fin + len_year + 10000

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
#dt = (t_ver[1:] - t_ver[:-1])
#print(dt/86400)

#=====================================================
sp.kclear()


with open(f"data/{t_ver[0]}_{t_ver[-1]}", 'wb') as f:
    pickle.dump(t_ver, f)



