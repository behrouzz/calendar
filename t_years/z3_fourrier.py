import numpy as np
from glob import glob
import pickle
import matplotlib.pyplot as plt

files = glob('data/*')

ls = []
for file in files:
    with open(file, 'rb') as f:
        arr = pickle.load(f)
    ls.append(arr)

arr = np.array([i for sublist in ls for i in sublist])
arr = np.sort(arr)

dt = (arr[:-1] - arr[1:])

x = range(len(dt))
y = dt.mean() - dt


fft = np.fft.fft(y)
a = np.abs(fft)

plt.plot(a)
plt.show()

from statsmodels import api as sm
acf = sm.tsa.acf(y, nlags=len(y))
lag = np.arange(len(y))
plt.plot(lag[:1000], acf[:1000])
plt.show()

##plt.plot(x, y, alpha=0.5)
##plt.scatter(x, y, c='r', s=10, alpha=0.5)
##plt.grid()
##plt.show()
