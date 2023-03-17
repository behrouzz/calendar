# gcc -fPIC -shared -o nut.so nut.c

import ctypes as ct
import numpy as np
import os

current_folder = os.getcwd()

lib = ct.CDLL(current_folder + '/nut.so')

func = lib.rotmat_2006a

func.argtypes = [ct.c_double, ct.c_double]
func.restype = ct.c_int

# out-parameters
a = ct.c_double()
b = ct.c_double()
c = ct.c_double()
d = ct.c_double()
e = ct.c_double()
f = ct.c_double()
g = ct.c_double()
h = ct.c_double()
i = ct.c_double()


def gcrs_to_tete(pos_gcrs, jd):
    
    d1 = jd
    d2 = 0.0
    
    _ = func(d1, d2,
             ct.byref(a), ct.byref(b), ct.byref(c),
             ct.byref(d), ct.byref(e), ct.byref(f),
             ct.byref(g), ct.byref(h), ct.byref(i))

    rot = np.array([[a.value, b.value, c.value],
                    [d.value, e.value, f.value],
                    [g.value, h.value, i.value]])

    return np.matmul(rot, pos_gcrs)

#=========================================================

import spiceypy as sp
from scipy import interpolate
from scipy.optimize import fsolve
from hypatie import car2sph
import pickle


def get_sun_gcrs(et):
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    return pos[:3] #GCRS

kernels = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
#sp.furnsh(kernels+'de441_part-1.bsp')
sp.furnsh(kernels+'de441_part-2.bsp')
sp.furnsh(kernels+'naif0012.tls')
#------------------------------------------
# 2451624 = 2000-03-20 12:00:00


jd0 = 2451624
jds = np.linspace(jd0-5, jd0+5, 1000)

decs = []
for jd in jds:
    et = sp.str2et('JD' + str(jd) + 'UTC')
    pos_gcrs = get_sun_gcrs(et)
    pos_tete = gcrs_to_tete(pos_gcrs, jd)
    ra, dec, r = car2sph(pos_tete)
    decs.append(dec)
decs = np.array(decs)
i_min = np.argmin(np.abs(decs))

for cnt in range(5):
    jd1 = jds[i_min-1]
    jd2 = jds[i_min+1]
    jds = np.linspace(jd1, jd2, 1000)
    decs = []
    for jd in jds:
        et = sp.str2et('JD' + str(jd) + 'UTC')
        pos_gcrs = get_sun_gcrs(et)
        pos_tete = gcrs_to_tete(pos_gcrs, jd)
        ra, dec, r = car2sph(pos_tete)
        decs.append(dec)
    decs = np.array(decs)
    i_min = np.argmin(np.abs(decs))
    dt_sec = (jds[i_min+1] - jds[i_min-1]) * 86400
    print(dt_sec, ':', decs[i_min])

print()
print('Vernal (JD-UTC):', jds[i_min])

#f = interpolate.interp1d(ets, dec, kind='cubic')


#------------------------------------------
sp.kclear()


