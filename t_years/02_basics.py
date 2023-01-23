import spiceypy as sp
import numpy as np
from glob import glob




adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
kernels = glob(adr+'naif*.tls') + [
    #adr+'de440.bsp',
    adr+'de441_part-1.bsp',
    #adr+'de441_part-2.bsp',
    ]

for k in kernels:
    sp.furnsh(k)
#===========================================

files = glob('data/*')

et1 = min([float(i.split('_')[0].split('\\')[-1]) for i in files])
et2 = min([float(i.split('_')[-1]) for i in files])

t1 = sp.etcal(et1)
t2 = sp.etcal(et2)

print(t1, ' : ', t2)
print(et1, ' : ', et2)

#===========================================
sp.kclear()
