import numpy as np

jd0 = 2451623.8159813415

cnt = 0
while jd0 > 2305447.4995233:
    jds = np.linspace(jd0-365.4, jd0-365.1, 1000)
    jd0 = jds[-1]
    cnt+=1

