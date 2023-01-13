#import numpy as np
import spiceypy as sp
from funcs import *

sp.furnsh('kernel.tm')
#=====================================================

ets, ras, decs, rasJ2000, decsJ2000, inds = equinox(year=-5000, steps=10000)
i_spring, i_summer, i_autumn, i_winter = inds

print('Vernal equinox J2000:', (rasJ2000[i_spring], decsJ2000[i_spring]))

show_seasons(ets, ras, decs, inds, plot=True)

#=====================================================
sp.kclear()
