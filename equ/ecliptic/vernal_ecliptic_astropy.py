from datetime import datetime, timedelta
import spiceypy as sp
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, GeocentricTrueEcliptic
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import fsolve


t0 = datetime(2023,3,20)
N = 24
ts = np.array([t0+timedelta(hours=i) for i in range(N)])

#==================================================
sp.furnsh("kernel_after_1969-07-30.tm")
ets = [sp.str2et(str(i)) for i in ts]
sun_icrs_raw = np.zeros((N,3))
for i, et in enumerate(ets):
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 0)
    sun_icrs_raw[i,:] = pos[:3]
sp.kclear()
#==================================================

x = sun_icrs_raw[:,0] * u.km
y = sun_icrs_raw[:,1] * u.km
z = sun_icrs_raw[:,2] * u.km

sun_icrs = SkyCoord(x=x, y=y, z=z, frame='icrs', representation_type='cartesian')

Ts = Time(ts)

ecls = [GeocentricTrueEcliptic(obstime=i, equinox=i) for i in Ts]
sun_ecl = [sun_icrs[i].transform_to(ecls[i]) for i in range(N)]

#================================

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

