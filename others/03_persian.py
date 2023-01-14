# error in N>=152386 and N>=182563
# check here:
# https://ssd.jpl.nasa.gov/tools/jdc/#/cd
# the date before 1500-03-01 should be 1500-02-29 but python gives: 1500-02-28


import numpy as np
from datetime import datetime, timedelta
import jdatetime as jdt
from persian import *

T0 = jdt.datetime(1378,10,11, 12)
t0 = datetime(2000, 1, 1, 12)

n = 152386
dt = [t0 - timedelta(days=i) for i in range(n, n+10)]
dT = [T0 - timedelta(days=i) for i in range(n, n+10)]

for i in range(len(dt)):
    print(i)
    print(dt[i])
    print(dT[i])
    print(dt_to_jd(dt[i]))
    print(julien(dT[i]))
    print('-'*10)

# https://github.com/slashmili/python-jalali/blob/main/jdatetime/jalali.py
# https://github.com/peykar/pgtkcalendar/blob/master/utility.py
