import numpy as np
import spiceypy as sp
from hypatie import car2sph
import matplotlib.pyplot as plt



def et_to_calender(et): #utc
    return sp.et2utc(et, 'C', 14, 26)


def et_to_jd(et): #utc
    return sp.et2utc(et, 'J', 14, 26)


def get_sun(et):
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sun_gcrs = pos[:3]
    rotmat = sp.sxform('J2000', 'ECLIPDATE', et)[:3,:3]
    sun_ec = np.matmul(rotmat, sun_gcrs)
    return car2sph(sun_gcrs), car2sph(sun_ec)


def equinox_calculations(year, month, day, delta_days, steps):
    if year <= 0:
        bcad = 'B.C.'
        year = str(year).replace('-', '')
    else:
        bcad = 'A.D.'
        year = str(year)
    t = f"{year} {bcad} {month} {day} 00:00:00"
    et = sp.str2et(t)
    delta = delta_days*86400
    ets = np.linspace(et, et+delta, steps)

    ras = np.zeros((len(ets),))
    decs = np.zeros((len(ets),))
    lons = np.zeros((len(ets),))
    lats = np.zeros((len(ets),))

    for i in range(len(ets)):
        gcrs, ecliptic = get_sun(ets[i])
        ras[i], decs[i], _ = gcrs
        lons[i], lats[i], _ = ecliptic

    return ets, ras, decs, lons, lats


def get_equinox(year, month=3, day=15, delta_days=10, steps=1000):
    kernel = "kernel_before_1969-07-30.tm" if year<=1969 else "kernel_after_1969-07-30.tm"
    sp.furnsh(kernel)
    ets, ras, decs, lons, lats = equinox_calculations(year, month, day, delta_days, steps)
    i_ver = np.argmax(lons)
    if (lons[i_ver]<359) or ((lons[i_ver]>360)): # check
        print('WARNING: very bad precesion!')
    ver_et = ets[i_ver]
    ver_jd = et_to_jd(ver_et)
    ver_cal = et_to_calender(ver_et)
    sp.kclear()
    return ver_et, ver_jd, ver_cal




