# year 1 of the Julian Period was 4713 BC (−4712)
# Julian calendar year 2023 is year 6736 of the current Julian Period

"""
The Julian day number (JDN) is the integer assigned to a whole solar day
in the Julian day count starting from noon Universal Time, with Julian
day number 0 assigned to the day starting at noon on Monday, January 1,
4713 BC, proleptic Julian calendar (November 24, 4714 BC, in the
proleptic Gregorian calendar). For example, the Julian day number for
the day starting at 12:00 UT (noon) on January 1, 2000, was 2451545.
"""

import numpy as np
from datetime import datetime, timedelta

def is_leap(y):
    c1 = (y%4 == 0)
    c2 = (y%100 != 0)
    c3 = (y%400 == 0)
    cond = (c1 and c2) or c3
    return cond


def day_of_year(y, m, d):
    yy = 2000 if is_leap(y) else 2023
    return datetime(yy, m, d).timetuple().tm_yday


def days_between_years(y1, y2):
    days = 0
    y2, y1 = y2-1, y1+1 # exclude y1 & y2
    while y2 >= y1:
        y_days = 366 if is_leap(y2) else 365
        days = days + y_days
        y2 = y2 - 1
    return days



date1 = (1999, 12, 30)
date2 = (2000, 1 , 31)


def days_between_dates(date1, date2):
    # Note: date1 < date2
    y1,m1,d1 = date1
    y2,m2,d2 = date2
    y1_days = 366 if is_leap(y1) else 365
    day1 = day_of_year(y1, m1, d1)
    day2 = day_of_year(y2, m2, d2)
    days_y1_y2 = days_between_years(y1, y2)
    result = days_y1_y2 + day2 + (y1_days-day1)
    return result


##date1 = (1, 1, 1)
##date2 = (2023, 11, 24)
##d = days_between_dates(date1, date2)
##print(d)

# group of 2820 years
# current 2820-year cycle began in 1096 CE (hejri:475)
y = 475

year = y -1

leaps = []
cycles = np.zeros((22,4))
for i in range(21):
    cycles[:-1, :] = [29, 33, 33, 33]
cycles[-1, :] = [29, 33, 33, 37]
cycles = cycles.flatten().astype(int)

for c in cycles:
    for i in range(c):
        year += 1
        if (i!=0) and ((i%4)==0):
            leaps.append(year)
        

