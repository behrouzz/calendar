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

#kernels = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
kernels = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
sp.furnsh(kernels+'de441_part-1.bsp')
#sp.furnsh(kernels+'de441_part-2.bsp')
#sp.furnsh(kernels+'de440.bsp')
sp.furnsh(kernels+'naif0012.tls')
#------------------------------------------

def get_min_index(JDS):
    DECS = []
    for JD in JDS:
        et = sp.str2et('JD' + str(JD) + 'TDT')
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
    

def run(y0, jd0, n_years):
    vernals = []
    years = []
    for i in range(1, n_years+1):
        jds = np.linspace(jd0-365.4, jd0-365.1, 1000)
        i_min, decs = get_min_index(jds)
        jd0 = kh_interpolate(x=jds, y=decs, guess=jds[i_min])
        vernals.append(jd0)
        years.append(y0-i)
    return np.array(vernals), np.array(years)


def read_jd0():
    file = 'data/before-1600.txt'
    with open(file) as f:
        for line in f:
            pass
        last_line = line
    y0 = int(last_line.split(',')[0].strip())
    jd0 = float(last_line.split(',')[-1].strip())
    return y0, jd0


y0, jd0 = read_jd0()
print('Start year & jd:', y0, jd0)

t1 = time.time()
vers, years = run(y0, jd0, n_years=1000)
t2 = time.time()
print('Calculation time (s):', t2-t1)

file = open('data/before-1600.txt', 'a')
for i,j in zip(years,vers):
    file.write(str(i)+','+str(j)+'\n')
file.close()


#------------------------------------------
sp.kclear()

#https://ssd.jpl.nasa.gov/tools/jdc/#/jd
