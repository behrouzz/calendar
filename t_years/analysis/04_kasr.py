import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels import api as sm


df = pd.read_csv('full.csv')

year = df['date'].str[:-6].astype(int).values
i_after2000 = np.where(year>=2000)[0]

df['dt'] = df['et'].diff().values/86400

df['kasr'] = df['dt'] - 365


df = df.iloc[i_after2000[:100]]
