from percal import *
import spiceypy as sp
import pandas as pd

df = pd.read_csv('t_years/analysis/equinox_time.csv').iloc[5000:5002]
#a = df[df['greg_year']==2000]

##def et2jd(et):
##    J2000 = 2451545.0
##    return J2000 + (et / 86400)


df['jd'] = (df['et']/86400) + 2451545.0

gregs1 = []
for i, v in df.iterrows():
    gregs1.append(Gregorian(v['greg_year'], v['greg_month'], v['greg_day']))

gregs2 = df['jd'].apply(lambda x: gregorian_from_jd(x))
pers = df['jd'].apply(lambda x: persian_from_jd(x))

jd = df.iloc[0]['jd']
print(jd)
print(gregs1[0])
print(gregs2.iloc[0])
print(pers.iloc[0])
print()

sp.furnsh('C:/Moi/_py/Astronomy/Solar System/kernels/naif0012.tls')

a = sp.str2et(f'{jd} JD TDT')
print('jd TDT 2 et :', a)
print('real et     :', df.iloc[0]['et'])

##b = sp.etcal(df.iloc[0]['et'], 40)
##c = sp.str2et(b + ' TDT')
##print(b)
##print(c)
##d1 = sp.str2et('8200 B.C. MAY 29 UTC')
##d2 = sp.str2et('8200 B.C. MAR 27 TDT')
##print(d1)
##print(d2)
sp.kclear()
