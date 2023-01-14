import numpy as np
from datetime import datetime, timedelta
from hypatie.time import datetime_to_jd

t0 = datetime(2000, 1, 1, 12) #2451545
jd0 = 2451545

#N = 152386 # error in N>=152386

for N in range(152380,152390):
    print(N)
    dt = [t0 - timedelta(days=i) for i in range(N)]
    djd = [jd0-i for i in range(N)]
    print(dt[-1])
    real_jd = djd[-1]
    calculated = datetime_to_jd(dt[-1])
    if round(calculated)!=real_jd:
        print('X'*50)
    print('-'*40)
