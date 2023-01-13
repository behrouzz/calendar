#import numpy as np
import spiceypy as sp
from funcs import *

sp.furnsh('kernel.tm')
#=====================================================

ets, ras, decs, inds = equinox(year=-600, steps=10000)
i_spring, i_summer, i_autumn, i_winter = inds

show_seasons(ets, ras, decs, inds, plot=False)

#=====================================================
sp.kclear()
