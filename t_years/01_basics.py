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
et = float(files[0].split('_')[-1])

t = sp.et2datetime(et)

print(et)
print(t)

#===========================================
sp.kclear()
