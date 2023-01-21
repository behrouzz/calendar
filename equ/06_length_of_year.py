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
from loy import *
import numpy as np
#from datetime import datetime
from scipy import interpolate
from scipy.optimize import fsolve


sp.furnsh('kernel.tm')
#sp.furnsh('kernel_after_1969-07-30.tm')
#sp.furnsh('kernel_before_1969-07-30.tm')
#=====================================================
ET0 = 6809763.812612681

y_ini = ET0
y_fin = -24747145.275395036 # t_ver of 1999


t_ver = []
for tekrar in range(10):
    len_year = y_ini - y_fin

    t1 = y_fin - len_year - 10000
    t2 = y_fin - len_year + 10000

    ets = np.linspace(t1, t2, 10000)

    dec = np.zeros((len(ets),))
    for i, et in enumerate(ets):
        _, dec[i], _, _ = true_sun(et)

    i_ver = np.argmin(np.abs(dec))

    if np.abs(dec).min()>0.001: # check accuracy
        print('WARNING:', np.abs(dec).min())

    f = interpolate.interp1d(ets, dec, kind='cubic')
    root = fsolve(f, ets[i_ver])[0]
    print(root)
    t_ver.append(root)

    y_ini = y_fin
    y_fin = root

t_ver = np.array(t_ver)
dt = (t_ver[:-1] - t_ver[1:])
print(dt/86400)
#=====================================================
sp.kclear()


# https://www.thetropicalevents.com/
# http://web.archive.org/web/20010502085156/http://home.earthlink.net/~scassidy/
