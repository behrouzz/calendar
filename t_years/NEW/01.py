# gcc -fPIC -shared -o nut.so nut.c

import ctypes as ct
import numpy as np

lib = ct.CDLL("C:/Users/behro/Desktop/JUST_TEST/Mov/c/Library/05_SOFA_nut_kh/py/nut.so")

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


sp.furnsh('kernel.tm')

jd = 2454000
et = sp.str2et('JD' + str(jd) + 'UTC') #TDT, TDB
print(et)

pos_gcrs = get_sun_gcrs(et)
pos_tete = gcrs_to_tete(pos_gcrs, jd)
ra, dec, r = car2sph(pos_tete)

sp.kclear()

#=========================================================

