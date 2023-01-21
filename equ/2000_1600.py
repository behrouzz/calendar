"""
vernam equinox of 2000:
-----------------------
2000 MAR 20 07:34:59.6270039733 UTC
or: ET0 = 6809763.812612681

So, I define ET0 as the origin of time.

1999 MAR 21 01:46:30.5389961376
2000 MAR 20 07:34:59.6270039733
2001 MAR 20 13:31:01.1989628076

-24747145.275395036
6809763.812612681
38367125.384571426
"""

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


sp.furnsh('H21.tm')
#=====================================================
ET0 = 6809763.812612681

y_ini = ET0
y_fin = -24747145.275395036 # t_ver of 1999


t_ver = []
while y_fin > -12622824000: # 1600-01-01 TDT
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
    #print(root)
    t_ver.append(root)

    y_ini = y_fin
    y_fin = root

t_ver = np.array([ET0, -24747145.275395036] + t_ver)
#dt = (t_ver[:-1] - t_ver[1:])
#print(dt/86400)

#=====================================================
#print(sp.et2datetime(ET0 -(dt.mean()*500)))
#print(sp.str2et('1600-01-01 TDT'))
sp.kclear()


with open(f"{t_ver[0]}_{t_ver[-1]}", 'wb') as f:
    pickle.dump(t_ver, f)

# https://www.thetropicalevents.com/
# http://web.archive.org/web/20010502085156/http://home.earthlink.net/~scassidy/



