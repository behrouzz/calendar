import spiceypy as sp
import numpy as np
from glob import glob
import pickle
import matplotlib.pyplot as plt


#adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
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

N = 500
#x = range(N)
#y = (dt[:N]).mean() - (dt[:N])
x = range(len(dt))
y = dt.mean() - dt


fft = np.fft.fft(y)
a = np.abs(fft)

plt.plot(x, y, alpha=0.5)
#plt.scatter(x, y, c='r', s=10, alpha=0.5)
plt.grid()
plt.show()

##et = float(files[0].split('_')[-1])
##t = sp.etcal(et)


#===========================================
sp.kclear()
