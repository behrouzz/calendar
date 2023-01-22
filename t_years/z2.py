import spiceypy as sp
import numpy as np
from glob import glob
import pickle
import matplotlib.pyplot as plt


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

ls = []
for file in files:
    with open(file, 'rb') as f:
        arr = pickle.load(f)
    ls.append(arr)

arr = np.array([i for sublist in ls for i in sublist])
arr = np.sort(arr)

dt = (arr[:-1] - arr[1:])

plt.plot(dt[:1000]/86400)
plt.show()

##et = float(files[0].split('_')[-1])
##t = sp.etcal(et)


#===========================================
sp.kclear()
