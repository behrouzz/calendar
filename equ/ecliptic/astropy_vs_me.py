from datetime import datetime, timedelta
import spiceypy as sp
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, GeocentricTrueEcliptic
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import fsolve
from hypatie.iau import precession, nutation, create_phi, B
from hypatie.time import utc2tdb, datetime_to_jd
from hypatie import car2sph



t0 = datetime(2023,3,20)
N = 24
ts = np.array([t0+timedelta(hours=i) for i in range(N)])

#==================================================
sp.furnsh("kernel_after_1969-07-30.tm")
ets = [sp.str2et(str(i)) for i in ts]
sun_icrs_raw = np.zeros((N,3))
earth_icrs_raw = np.zeros((N,3))
for i, et in enumerate(ets):
    sun, _ = sp.spkez(10, et, 'J2000', 'LT+S', 0)
    earth, _ = sp.spkez(399, et, 'J2000', 'LT+S', 0)
    sun_icrs_raw[i,:] = sun[:3]
    earth_icrs_raw[i,:] = earth[:3]
sp.kclear()
#==================================================
# khodam
# ======

def tete_rotmat_and_eps(t):
    t = utc2tdb(t)
    T = (datetime_to_jd(t) - 2451545) / 36525
    P = precession(T)
    d_psi, d_e, e, _, _, _ = create_phi(T)
    N = nutation(d_psi, d_e, e)
    rot_mat = np.matmul(np.matmul(N, P), B)
    return rot_mat, e, d_e


def tete_to_trueecliptic(pos_tete, d_eps_prin):
    # ref: http://www.astrosurf.com/jephem/astro/ephemeris/et520transfo_en.htm
    r1 = [1,0,1]
    r2 = [1, np.cos(d_eps_prin), np.sin(d_eps_prin)]
    r3 = [0, -np.sin(d_eps_prin), np.cos(d_eps_prin)]
    mat = np.array([r1, r2, r3])
    return np.matmul(mat, pos_tete)

pos_ecl_car = np.zeros((N,3))
for i, t in enumerate(ts):
    rot_mat, e, d_e = tete_rotmat_and_eps(t)
    pos_gcrs = sun_icrs_raw[i,:] - earth_icrs_raw[i,:]
    pos_tete = np.matmul(rot_mat, pos_gcrs)
    d_eps_prin = e + d_e # GHALAT!!!
    pos_ecl_car[i,:] = tete_to_trueecliptic(pos_tete, d_eps_prin) # GHALAT!!!
pos_ecl_sph = car2sph(pos_ecl_car)# GHALAT!!!
#==================================================
# Astropy
# =======

x = sun_icrs_raw[:,0] * u.km
y = sun_icrs_raw[:,1] * u.km
z = sun_icrs_raw[:,2] * u.km

sun_icrs = SkyCoord(x=x, y=y, z=z, frame='icrs', representation_type='cartesian')

Ts = Time(ts)

ecls = [GeocentricTrueEcliptic(obstime=i, equinox=i) for i in Ts]
sun_ecl = [sun_icrs[i].transform_to(ecls[i]) for i in range(N)]

#================================
# Interpolate
# ===========

lons = np.array([sun_ecl[i].lon.value for i in range(N)])
i_max = np.argmax(lons)
lons_cont = np.where(lons>300, lons, lons+360)

t_sec = np.array([i.total_seconds() for i in (ts-ts[0])])

f = interpolate.interp1d(t_sec, lons_cont-360, kind='linear') #cubic

root = fsolve(f, t_sec[i_max])[0]
t_exact = t0 + timedelta(seconds=root)
print(t_exact)

plt.plot(ts, lons_cont)
plt.scatter(ts[i_max:i_max+2], lons_cont[i_max:i_max+2], c='g')
plt.scatter(t_exact, 360, c='r')
plt.show()

