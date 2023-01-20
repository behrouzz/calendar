import spiceypy as sp
from funcs import *
import pickle

sp.furnsh('kernel.tm')
#sp.furnsh('kernel_after_1969-07-30.tm')
#=====================================================
points = []

for yr in range(-3000, 2000, 500):
    ets, ras, decs, rasJ2000, decsJ2000, i_ver, t = vernal(year=yr, steps=10000)
    ver_ra, ver_dec = rasJ2000[i_ver], decsJ2000[i_ver]
    points.append((ver_ra, ver_dec, str(yr), str(yr)))
    print(yr, 'Spring:', t)


#=====================================================
sp.kclear()


from baladin import Aladin

a = Aladin(target='68.9801627900154 16.5093023507718', fov=90)

##markers = [
##    (0, 0, 'Vernal Equionox', 'J2000'),
##    (68.9801627900154, 16.5093023507718, 'aldebaran', 'aldebaran'),
##    (31.79335709957655, 23.46241755020095, 'Hamal', 'alf Aries'),
##    ]


a.add_markers(points)
a.create()
a.save('index.html')

