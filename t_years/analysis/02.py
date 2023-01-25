import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('ets_cal.csv', dtype={'et':str})

bc = df['cal'].str.contains('B.C.')
ad = ~df['cal'].str.contains('B.C.')


years =  list(df['cal'].str.split(' '))
df['year'] = [int(i[0]) for i in years]
df.loc[bc, 'year'] = -df.loc[bc, 'year']

df['cal'] = df['cal'].str.replace('B.C. ', '')
df['cal'] = df['cal'].str.replace('A.D. ', '')

months = list(df['cal'].str.split(' '))
df['month'] = [i[1] for i in months]
df['month'] = df['month'].str.replace('MAR', '03')
df['month'] = df['month'].str.replace('APR', '04')
df['month'] = df['month'].str.replace('FEB', '02')

days = list(df['cal'].str.split(' '))
df['day'] = [i[2] for i in days]

times = list(df['cal'].str.split(' '))
df['time'] = [i[-1] for i in times]

df['date'] = df['year'].astype(str) + '-' + df['month'] + '-' + df['day']

df[['et', 'date', 'time']].set_index('et').to_csv('full.csv')
