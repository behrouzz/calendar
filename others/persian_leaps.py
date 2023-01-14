
"""
Module leaps
------------
Calcute leap years in the Proleptic Persian Calendar

Ref: https://www.timeanddate.com/date/iran-leap-year.html

# group of 2820 years
# current 2820-year cycle began in 1096 CE (hejri:475)

period = -2 # -5165 to -2346
period = -1 # -2345 to 474
period = 0  # 475 to 3294
period = 1  # 3295 to 6114
period = 2  # 6115 to 8934
"""

import numpy as np


MONTHSDAYS_COMMUN = np.array([31,31,31,31,31,31, 30,30,30,30,30,29])
MONTHSDAYS_LEAPS  = np.array([31,31,31,31,31,31, 30,30,30,30,30,30])


def create_future_periods(until=50000):
    ps = []
    t1 = 475
    while t1<until:
        t2 = t1 + 2819
        ps.append([t1, t2])
        t1 = t2 + 1
    return np.array(ps)
    

def create_historic_periods(since=-50000):
    ps = []
    t2 = 475 - 1
    while t2>since:
        t1 = t2 - 2819
        ps.append([t1, t2])
        #t1 = t2 + 1
        t2 = t1 - 1
    return np.array(ps)


def get_period(yr):
    if yr < 475:
        ps = create_historic_periods()
        period = ps[ps[:,0]<yr][0]
    elif yr > 475:
        ps = create_future_periods()
        period = ps[ps[:,0]<yr][-1]
    else: # yr==475
        ps = create_future_periods()
        period = ps[0]
    return period


def leaps_in_current_period(yr):
    y0 = get_period(yr)[0]

    year = y0 -1

    arr_leaps = []
    cycles = np.zeros((22,4))
    for i in range(21):
        cycles[:-1, :] = [29, 33, 33, 33]
    cycles[-1, :] = [29, 33, 33, 37]
    cycles = cycles.flatten().astype(int)

    for c in cycles:
        for i in range(c):
            year += 1
            if (i!=0) and ((i%4)==0):
                arr_leaps.append(year)
    arr_leaps = np.array(arr_leaps)
    return arr_leaps


def is_leapyear(year):
    arr_leaps = leaps_in_current_period(year)
    return year in arr_leaps


def matrix_days(year):
    if is_leapyear(year):
        monthsdays = MONTHSDAYS_LEAPS
    else:
        monthsdays = MONTHSDAYS_COMMUN

    arr = np.zeros((monthsdays.sum(),3))

    dayofyear = 0
    for i,m in enumerate(monthsdays):
        for dayofmonth in range(1,m+1):
            dayofyear += 1
            arr[dayofyear-1, :] = [dayofyear, i+1, dayofmonth]

    arr = arr.astype(int)
    return arr


def day_of_year(y, m, d):
    arr = matrix_days(y)
    return arr[np.logical_and((arr[:,1]==m),(arr[:,2]==d))][0][0]


def days_between_years(y1, y2):
    days = 0
    y2, y1 = y2-1, y1+1 # exclude y1 & y2
    while y2 >= y1:
        y_days = 366 if is_leapyear(y2) else 365
        days = days + y_days
        y2 = y2 - 1
    return days


def days_between_dates(date1, date2):
    # Note: date1 < date2
    y1,m1,d1 = date1
    y2,m2,d2 = date2
    y1_days = 366 if is_leapyear(y1) else 365
    day1 = day_of_year(y1, m1, d1)
    day2 = day_of_year(y2, m2, d2)
    days_y1_y2 = days_between_years(y1, y2)
    result = days_y1_y2 + day2 + (y1_days-day1)
    return result
