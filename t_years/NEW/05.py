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
import time


def get_sun_gcrs(et):
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    return pos[:3] #GCRS

kernels = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
#sp.furnsh(kernels+'de441_part-1.bsp')
sp.furnsh(kernels+'de441_part-2.bsp')
sp.furnsh(kernels+'naif0012.tls')
#------------------------------------------

def get_min_index(jds):
    decs = []
    for jd in jds:
        et = sp.str2et('JD' + str(jd) + 'UTC')
        pos_gcrs = get_sun_gcrs(et)
        pos_tete = gcrs_to_tete(pos_gcrs, jd)
        ra, dec, r = car2sph(pos_tete)
        decs.append(dec)
    decs = np.array(decs)
    i_min = np.argmin(np.abs(decs))
    return i_min, decs




# 2451624 = 2000-03-20 12:00:00
vernal_2000 = 2451623.8159813415

jd0 = vernal_2000

vernals = [jd0]

t1 = time.time()
for tekrar in range(10):
    jds = np.linspace(jd0-365.4, jd0-365.1, 1000)
    i_min, _ = get_min_index(jds)

    ls = [0]
    for cnt in range(5):
        jd1 = jds[i_min-1]
        jd2 = jds[i_min+1]
        jds = np.linspace(jd1, jd2, 1000)
        i_min, decs = get_min_index(jds)
        dt_sec = (jds[i_min+1] - jds[i_min-1]) * 86400
        if jds[i_min]==ls[-1]:
            break
        ls.append(jds[i_min])

    jd0 = jds[i_min]
    vernals.append(jd0)

t2 = time.time()

print(t2-t1)
#f = interpolate.interp1d(ets, dec, kind='cubic')


#------------------------------------------
sp.kclear()


