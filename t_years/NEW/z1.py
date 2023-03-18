import spiceypy as sp

kernels = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'

sp.furnsh(kernels+'naif0012.tls')

et1 = sp.str2et('1600 JAN 1 00:00:00 TDT')
et2 = sp.str2et('2600 SEP 1 00:00:00 TDT')
a1 = sp.et2utc(et1, 'J', 14, 30)
a2 = sp.et2utc(et2, 'J', 14, 30)

sp.kclear()

"""
>>> a1
'JD 2305447.4995233'
>>> a2
'JD 2670933.4991993'
"""



