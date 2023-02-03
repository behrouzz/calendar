import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



"""
MAKE_EPHEM=YES
COMMAND=10
EPHEM_TYPE=OBSERVER
CENTER='500@399'
START_TIME='B.C. 9998-01-01 00:00'
STOP_TIME='A.D. 9999-01-01 00:00'
STEP_SIZE='1 YEARS'
QUANTITIES='30'
REF_SYSTEM='ICRF'
CAL_FORMAT='BOTH'
TIME_DIGITS='SECONDS'
ANG_FORMAT='DEG'
APPARENT='AIRLESS'
RANGE_UNITS='KM'
SUPPRESS_RANGE_RATE='NO'
SKIP_DAYLT='NO'
SOLAR_ELONG='0,180'
EXTRA_PREC='NO'
RTS_ONLY='NO'
CSV_FORMAT='YES'
OBJ_DATA='NO'
"""

with open('data/BC9998_AD9999.txt', 'r') as f:
    all_text = f.read()

mark1 = all_text.find('$$SOE')
text = all_text[mark1+6:]
mark2 = text.find('$$EOE')
text = text[:mark2]
raw_rows = text.split('\n')[:-1]


raw_rows = [i.split(',')[:-1] for i in raw_rows]
rows = []
for r in raw_rows:
    row = [i.strip() for i in r]
    row = [i for i in row if len(i)>0]
    rows.append(row)

rows = [[i[0], float(i[1]), float(i[2])] for i in rows]

jd = np.array([i[1] for i in rows])
dut = np.array([i[2] for i in rows])

plt.plot(jd, dut)
plt.show()
