
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
from .data import periods, per_jul, jul_per


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


def get_period_lowlevel(yr):
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


def get_period(yr):
    if (yr<-50285) or (yr>=51234):
        period = get_period_lowlevel(yr)
    else:
        period = periods[periods[:,0]<=yr][-1]
    return period


def periods_between_two_years(y1, y2):
    p1 = get_period(y1)
    p2 = get_period(y2)
    ind1 = np.where(periods==p1)[0][0]
    ind2 = np.where(periods==p2)[0][0]
    return periods[ind1:ind2+1]


def leaps_between_two_years(y1, y2):
    ps = periods_between_two_years(y1, y2)
    all_leaps = [list(leaps_in_current_period(p)) for p in ps]
    all_leaps = [i for sublist in all_leaps for i in sublist]
    return all_leaps


def leaps_in_current_period(period):
    y0 = period[0]

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


def leaps_in_period_of_this_year(yr):
    period = get_period(yr)
    return leaps_in_current_period(period)


def is_leapyear(year):
    arr_leaps = leaps_in_period_of_this_year(year)
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
    all_leaps = leaps_between_two_years(y1, y2)
    while y2 >= y1:
        y_days = 366 if (y2 in all_leaps) else 365
        days = days + y_days
        y2 = y2 - 1
    return days


def days_between_dates(date1, date2):
    y1,m1,d1 = date1
    y2,m2,d2 = date2
    if y1==y2:
        if m1==m2:
            if d1>d2:
                raise Exception('Note: date1 < date2')
        elif m1>m2:
            raise Exception('Note: date1 < date2')
    elif y1>y2:
        raise Exception('Note: date1 < date2')
    y1_days = 366 if is_leapyear(y1) else 365
    day1 = day_of_year(y1, m1, d1)
    day2 = day_of_year(y2, m2, d2)
    if y1==y2:
        result = day2 - day1
    else:
        days_y1_y2 = days_between_years(y1, y2)
        result = days_y1_y2 + day2 + (y1_days-day1)
    return result


def __add_days(date, delta):
    y,m,d = date
    y_days = 366 if is_leapyear(y) else 365
    day = day_of_year(y, m, d)
    mat = matrix_days(y)[day:]
    n = 0
    new_y = y

    if delta > y_days-day:
        while n < delta:
            new_y += 1
            new_mat = matrix_days(new_y)
            n = len(mat) + len(new_mat)
            if n > delta:
                mat = np.vstack((mat, new_mat))[:delta]
            else:
                mat = np.vstack((mat, new_mat))
        return (new_y, mat[-1, 1], mat[-1, 2])
    elif delta==0:
        return date
    else:
        return (new_y, mat[delta-1,1], mat[delta-1,2])
    

def __sub_days(date, delta):
    y,m,d = date
    y_days = 366 if is_leapyear(y) else 365
    day = day_of_year(y, m, d)
    n = 0
    new_y = y
    mat = matrix_days(y)[:day]

    while True:
        if abs(delta) > len(mat):
            new_y -= 1
            new_mat = matrix_days(new_y)
            mat = np.vstack((new_mat, mat))
            if len(mat) > abs(delta):
                result = tuple([new_y]+list(mat[delta-1, 1:]))
                break
            elif len(mat) == abs(delta):
                result = tuple([new_y-1]+list(matrix_days(new_y-1)[-1,1:]))
                break
        elif abs(delta) == len(mat):
            result = tuple([y-1]+list(matrix_days(y-1)[-1,1:]))
            break
        else: # abs(delta) < len(mat)
            result = tuple([y]+list(mat[delta-1, 1:]))
            break
    return result


def add_days(date, delta):
    if delta < 0:
        return __sub_days(date, delta)
    else:
        return __add_days(date, delta)


def persian_to_jd(date):
    y = date[0]
    y0 = y - (y%1000)
    jd0 = per_jul[y0]
    date0 = (y0, 1, 1)
    dt = days_between_dates(date0, date)
    return jd0 + dt


def jd_to_persian(jd):
    arr = np.array(list(per_jul.values()))
    jd0 = arr[arr<=jd].max()
    y0 = jul_per[jd0]
    date0 = (y0, 1, 1)
    return add_days(date0, int(jd-jd0))
