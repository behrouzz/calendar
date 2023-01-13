import spiceypy as sp
from funcs import *

sp.furnsh('kernel.tm')
#=====================================================

for yr in range(-1000, 1950, 50):
    ets, ras, decs, inds = equinox(year=yr, steps=10000)
    i_spring, i_summer, i_autumn, i_winter = inds
    print(yr, 'Spring:', et_to_calender(ets[i_spring]))


#=====================================================
sp.kclear()
