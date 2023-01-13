import spiceypy as sp
from funcs import *
import pickle

sp.furnsh('kernel.tm')
#=====================================================

#for yr in range(-1000, 1950, 50):

for yr in range(-3000, 2000, 1000):
    ets, ras, decs, rasJ2000, decsJ2000, inds = equinox(year=yr, steps=10000)
    i_spring, i_summer, i_autumn, i_winter = inds
    ver_ra, ver_dec = rasJ2000[i_spring], decsJ2000[i_spring]
    print(yr, ':', (ver_ra, ver_dec))
    
    #print(yr, 'Spring:', et_to_calender(ets[i_spring]))


#=====================================================
sp.kclear()
# aldebaran
# 68.9801627900154, 16.5093023507718
31.79335709957655, 23.46241755020095

from baladin import Aladin

a = Aladin(target='68.9801627900154 16.5093023507718', fov=90)

markers = [
    (0, 0, 'Vernal Equionox', 'J2000'),
    (68.9801627900154, 16.5093023507718, 'aldebaran', 'aldebaran'),
    (31.79335709957655, 23.46241755020095, 'Hamal', 'alf Aries'),
    ]
a.add_markers(markers)
a.create()
a.save('index.html')
