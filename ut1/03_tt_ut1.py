import pandas as pd
from iers import create_df, files_dc
import matplotlib.pyplot as plt

LOCAL = 'C:/Moi/_py/Astronomy/Earth/IERS/data/'
file = LOCAL + files_dc['hmnao_a_2021.eop']['adr'] + 'hmnao_a_2021.eop'
df = create_df(file)[['MJD','UT1-TAI']]
df['jd'] = df['MJD'] + 2400000.5
# tt = tai + 32.184
df['UT1-TT'] = df['UT1-TAI'] - 32.184

plt.plot(df['jd'], df['UT1-TT'])
plt.show()

"""
Date__(UT)__HR:MN:SS, Date_________JDUT

b9998-Jan-01 00:00:00, -1930346.5
"""
