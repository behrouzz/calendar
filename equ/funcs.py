import numpy as np
import spiceypy as sp
from hypatie import car2sph
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import fsolve


def sun_gcrs(et, abcorr='LT+S'):
    pos, _ = sp.spkez(10, et, 'J2000', abcorr, 399)
    return pos[:3]


def j2000_to_tete_rotmat(et):
    return sp.sxform('J2000', 'TETE', et)[:3,:3]


def et_to_calender(et):
    return sp.et2utc(et, 'C', 14, 32)


def true_sun(et):
    rotmat = j2000_to_tete_rotmat(et)
    sunJ2000 = sun_gcrs(et)
    raJ2000, decJ2000, _ = car2sph(sunJ2000)
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec, r = car2sph(sun)
    return ra, dec, raJ2000, decJ2000



def vernal(year, month=3, day=17, delta_days=10, steps=1000):
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

    decs = np.zeros((len(ets),))
    ras = np.zeros((len(ets),))
    rasJ2000 = np.zeros((len(ets),))
    decsJ2000 = np.zeros((len(ets),))
    for i in range(len(ets)):
        ras[i], decs[i], rasJ2000[i], decsJ2000[i] = true_sun(ets[i])

    i_ver = np.argmin(np.abs(decs))
    if np.abs(decs).min()>0.01:
        print('WARNING:', np.abs(decs).min())
    # interpolate
    f = interpolate.interp1d(ets, decs, kind='cubic')
    root = fsolve(f, ets[i_ver])[0]
    t_exact = et_to_calender(root)
    return ets, ras, decs, rasJ2000, decsJ2000, i_ver, t_exact



def equinox(year, steps=1000):
    if year <= 0:
        bcad = 'B.C.'
        year = str(year).replace('-', '')
    else:
        bcad = 'A.D.'
        year = str(year)
    t = f"{year} {bcad} 1 1 00:00:00"
    et = sp.str2et(t)
    delta = 365.24223*86400 #persian: 365.2421986
    ets = np.linspace(et, et+delta, steps)

    decs = np.zeros((len(ets),))
    ras = np.zeros((len(ets),))
    rasJ2000 = np.zeros((len(ets),))
    decsJ2000 = np.zeros((len(ets),))
    for i in range(len(ets)):
        ras[i], decs[i], rasJ2000[i], decsJ2000[i] = true_sun(ets[i])

    i_summer = np.argmax(decs)
    i_winter = np.argmin(decs)
    i1,i2 = np.abs(decs).argsort()[:2]
    if decs[i1-1]<decs[i1+1]:
        i_spring, i_autumn = i1, i2
    else:
        i_spring, i_autumn = i2, i1
    return ets, ras, decs, rasJ2000, decsJ2000, [i_spring, i_summer, i_autumn, i_winter]


def show_seasons(ets, ras, decs, inds, plot=True):
    i_spring, i_summer, i_autumn, i_winter = inds
    print('FROM:', et_to_calender(ets[0]))
    print('TO  :', et_to_calender(ets[-1]))
    print()
    print('Spring:', et_to_calender(ets[i_spring]))
    print('Summer:', et_to_calender(ets[i_summer]))
    print('Autumn:', et_to_calender(ets[i_autumn]))
    print('Winter:', et_to_calender(ets[i_winter]))

    if plot:
        fig, ax = plt.subplots()
        ax.plot(ets, decs)
        ax.axhline(y=0, c='k')
        ax.axvline(x=ets[i_spring], c='g', alpha=0.5, ls=':')
        ax.axvline(x=ets[i_summer], c='r',alpha=0.5, ls='-.')
        ax.axvline(x=ets[i_autumn], c='brown', alpha=0.5, ls=':')
        ax.axvline(x=ets[i_winter], c='b', alpha=0.5, ls='-.')
        plt.show()
