
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
from .data import periods, official_leaps
from.birashk import leaps_in_period_of_this_year

MONTHSDAYS_COMMUN = np.array([31,31,31,31,31,31, 30,30,30,30,30,29])
MONTHSDAYS_LEAPS  = np.array([31,31,31,31,31,31, 30,30,30,30,30,30])

MIN = (1206, 1 , 1 ) # 1827 MARS ?
MAX = (1498, 12, 30) # 2120 MARS ?


def is_leapyear(year, official=True):
    if official:
        return year in official_leaps
    else:
        arr_leaps = leaps_in_period_of_this_year(year)
        return year in arr_leaps


def leaps_between_two_years(y1, y2, official=True):
    if official:
        return official_leaps[np.logical_and(official_leaps>=y1,official_leaps<y2)]



def matrix_days(year, official=True):
    if is_leapyear(year, official):
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


def day_of_year(y, m, d, official=True):
    arr = matrix_days(y, official)
    return arr[np.logical_and((arr[:,1]==m),(arr[:,2]==d))][0][0]


def days_between_years(y1, y2, official=True):
    days = 0
    y2, y1 = y2-1, y1+1 # exclude y1 & y2
    all_leaps = leaps_between_two_years(y1, y2, official)
    while y2 >= y1:
        y_days = 366 if (y2 in all_leaps) else 365
        days = days + y_days
        y2 = y2 - 1
    return days


def days_between_dates(date1, date2, official=True):
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
    y1_days = 366 if is_leapyear(y1, official) else 365
    day1 = day_of_year(y1, m1, d1, official)
    day2 = day_of_year(y2, m2, d2, official)
    if y1==y2:
        result = day2 - day1
    else:
        days_y1_y2 = days_between_years(y1, y2, official)
        result = days_y1_y2 + day2 + (y1_days-day1)
    return result


def __add_days(date, delta, official=True):
    y,m,d = date
    y_days = 366 if is_leapyear(y, official) else 365
    day = day_of_year(y, m, d, official)
    mat = matrix_days(y, official)[day:]
    n = 0
    new_y = y

    if delta > y_days-day:
        while n < delta:
            new_y += 1
            new_mat = matrix_days(new_y, official)
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
    

def __sub_days(date, delta, official=True):
    y,m,d = date
    y_days = 366 if is_leapyear(y, official) else 365
    day = day_of_year(y, m, d, official)
    n = 0
    new_y = y
    mat = matrix_days(y, official)[:day]

    while True:
        if abs(delta) > len(mat):
            new_y -= 1
            new_mat = matrix_days(new_y, official)
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


def add_days(date, delta, official=True):
    if delta < 0:
        return __sub_days(date, delta, official)
    else:
        return __add_days(date, delta, official)


def persian_to_jd(date, official=True):
    # must be more rapid
    date0 = (-5334, 9, 2)
    return 0.5 + days_between_dates(date0, date, official)


def jd_to_persian(jd, official=True):
    date0 = (1378, 10, 11)
    jd0 = 2451544.5
    return add_days(date0, round(jd-jd0), official)
