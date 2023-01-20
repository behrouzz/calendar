import spiceypy as sp
from funcs import *
import numpy as np
from datetime import datetime

sp.furnsh('kernel.tm')
#sp.furnsh('kernel_after_1969-07-30.tm')
#=====================================================
years = np.arange(-15,-10)
times = []

for i, yr in enumerate(years):
    ets, ras, decs, rasJ2000, decsJ2000, i_ver, t = vernal(year=yr, steps=10000)
    times.append(t)

tmp = []
for i in times:
    if 'A.D.' in i:
        tmp.append(i[i.find('A.D.')+9:])
    elif 'B.C.' in i:
        tmp.append(i[i.find('B.C.')+9:])
    else:
        tmp.append(i)

times = tmp

#times = [i[i.find('A.D.')+9:] for i in times]


times2 = []
for i in times:
    if len(i.split('.')[-1])>6:
        times2.append(i.split('.')[-0] + '.' + i.split('.')[-1][:6])
    else:
        times2.append(i)

dt_times = []
for i, t in enumerate(times2):
    t_str = str(2000+years[i])+'-03-'+t
    dt_times.append(datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S.%f'))


lengths = []

for i in range(1, len(dt_times)):
    a = (dt_times[i] - dt_times[i-1]).total_seconds()
    a = a/86400
    if a<365:
        a += 1
    if a>366:
        a -= 1
    print(a)
               
#=====================================================
sp.kclear()
