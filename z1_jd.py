from percal import *
import spiceypy as sp
import pandas as pd

df = pd.read_csv('t_years/analysis/equinox_time.csv')


def et2day(et):
    return (et/86400) + 0.5

g = Gregorian(-13199, 4, 5)

df['D'] = (df['et']/86400) + 0.5

t2000 = Gregorian(2000, 1, 1)
jd0 = t2000.to_jd()


gregs = []
for i, v in df.iterrows():
    gregs.append(Gregorian(v['greg_year'], v['greg_month'], v['greg_day']))

JD = [i.to_jd() for i in gregs]
df['jd'] = JD

# Spice et <-> JD check
sp.furnsh('C:/Moi/_py/Astronomy/Solar System/kernels/naif0012.tls')

sp_jd = list(df['jd'].astype(str) + ' JD TDT')
sp_et = sp.str2et(sp_jd)

sp.kclear()
"""
et = 6809763.812613
a = sp.etcal(et, 40)
print(a)

sp.furnsh('C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/naif0012.tls')
b = sp.str2et('2000-01-01 00:00:00 TDT')
sp.kclear()
print(b)
"""
# sp.str2et('2451544.5 JD TDT')
# -43200.000087209555
