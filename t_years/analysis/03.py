import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels import api as sm


df = pd.read_csv('full.csv')

year = df['date'].str[:-6].astype(int).values
i_after2000 = np.where(year>=2000)[0]

dt = df['et'].diff().values[1:]

x = df['et'].iloc[1:].values
y = dt.mean() - dt

##plt.plot(x, y, alpha=0.5)
##plt.grid()
##plt.show()


fft = np.fft.fft(y)
a = np.abs(fft)

plt.plot(year[i_after2000-1], a[i_after2000-1])
plt.grid()
plt.show()



##acf = sm.tsa.acf(y, nlags=len(y))
##lag = np.arange(len(y))
##plt.plot(lag[:1000], acf[:1000])
##plt.grid()
##plt.show()

