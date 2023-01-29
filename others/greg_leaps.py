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
import calendar

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



#t0 = datetime(1,1,1)
#years = [t0 + timedelta(days=i) for i in range(2000*400)]

#c = calendar.Calendar()
#c = calendar.TextCalendar()

for y in range(1, 2100):
    kh = is_leap(y)
    a = calendar.isleap(y)
    #if kh!=a:
    if (kh + a)==1:
        print(y)
