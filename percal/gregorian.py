"""
Proleptic Gregorian Calendar
"""

import numpy as np
from .data import gre_jul, jul_gre


MONTHSDAYS_COMMUN = np.array([31,28,31,30,31,30, 31,31,30,31,30,31])
MONTHSDAYS_LEAPS  = np.array([31,29,31,30,31,30, 31,31,30,31,30,31])
MONTHSDAYS_1582   = np.array([31,29,31,30,31,30, 31,31,30,21,30,31])

def greg_leap_after1582(y):
    c1 = (y%4 == 0)
    c2 = (y%100 != 0)
    c3 = (y%400 == 0)
    cond = (c1 and c2) or c3
    return cond


def greg_leap(y):
    if y>=1582:
        return greg_leap_after1582(y)
    else:
        return (y%4)==0
        


def greg_leaps_between_two_years(y1, y2):
    return [i for i in range(y1,y2+1) if greg_leap(i)]


def matrix_days(year):
    if year==1582:
        monthsdays = MONTHSDAYS_1582
    else:
        if greg_leap(year):
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
    if (y1<1582) and (y2>1582):
        sub10 = True
    else:
        sub10 = False
    days = 0
    y2, y1 = y2-1, y1+1 # exclude y1 & y2
    all_leaps = greg_leaps_between_two_years(y1, y2)
    while y2 >= y1:
        y_days = 366 if (y2 in all_leaps) else 365
        days = days + y_days
        y2 = y2 - 1
    if sub10:
        days -= 10
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
    y1_days = 366 if greg_leap(y1) else 365
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
    y_days = 366 if greg_leap(y) else 365
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
    y_days = 366 if greg_leap(y) else 365
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


def gregorian_to_jd(date):
    y = date[0]
    y0 = y - (y%1000)
    jd0 = gre_jul[y0]
    date0 = (y0, 1, 1)
    dt = days_between_dates(date0, date)
    return jd0 + dt


def jd_to_gregorian(jd):
    arr = np.array(list(gre_jul.values()))
    jd0 = arr[arr<=jd].max()
    y0 = jul_gre[jd0]
    date0 = (y0, 1, 1)
    return add_days(date0, int(jd-jd0))
