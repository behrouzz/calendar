import spiceypy as sp
from funcs import *
import pickle

sp.furnsh('kernel.tm')
#=====================================================

#for yr in range(-1000, 1950, 50):

for yr in range(-2000, 0, 100):
    ets, ras, decs, rasJ2000, decsJ2000, inds = equinox(year=yr, steps=10000)
    i_spring, i_summer, i_autumn, i_winter = inds
    ver_ra, ver_dec = rasJ2000[i_spring], decsJ2000[i_spring]
    print(yr, ':', (ver_ra, ver_dec))
    
    #print(yr, 'Spring:', et_to_calender(ets[i_spring]))


#=====================================================
sp.kclear()
