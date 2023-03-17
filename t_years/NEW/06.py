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
#sp.furnsh(kernels+'de441_part-2.bsp')
sp.furnsh(kernels+'de440.bsp')
sp.furnsh(kernels+'naif0012.tls')
#------------------------------------------

def get_min_index(JDS):
    DECS = []
    for JD in JDS:
        et = sp.str2et('JD' + str(JD) + 'UTC')
        pos_gcrs = get_sun_gcrs(et)
        pos_tete = gcrs_to_tete(pos_gcrs, JD)
        ra, dec, r = car2sph(pos_tete)
        DECS.append(dec)
    DECS = np.array(DECS)
    i_MIN = np.argmin(np.abs(DECS))
    return i_MIN, DECS


def kh_interpolate(x, y, guess):
    f = interpolate.interp1d(x, y, kind='cubic', fill_value='extrapolate')
    root = fsolve(f, guess)[0]
    return root
    


# 2451624 = 2000-03-20 12:00:00
vernal_2000 = 2451623.8159813415

jd0 = vernal_2000

vernals = [jd0]

t1 = time.time()
for years in range(100):
    jds = np.linspace(jd0-365.4, jd0-365.1, 1000)
    i_min, decs = get_min_index(jds)

    jd0 = kh_interpolate(x=jds, y=decs, guess=jds[i_min])
    
    vernals.append(jd0)

t2 = time.time()
vernals = np.array(vernals)
print(t2-t1)


#------------------------------------------
sp.kclear()

##import matplotlib.pyplot as plt
##plt.plot(jds, decs)
##plt.scatter(jds, decs, c='r')
##plt.scatter(jds[i_min], decs[i_min], c='r')
###plt.scatter([jd0], decs[i_min], s=30, c='g')
##plt.grid()
##plt.show()
