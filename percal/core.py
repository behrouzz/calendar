import numpy as np
#from .data import periods, official_leaps
from .birashk import add_days, is_leapyear, day_of_year, jd_to_persian, persian_to_jd


def from_jd(jd):
    y,m,d = jd_to_persian(jd)
    return Persian(y,m,d)


class Persian:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.date = (year, month, day)

    def __repr__(self):
        return 'Persian'+str((self.year, self.month, self.day))

    def is_leap(self):
        return is_leapyear(self.year)

    def day_of_year(self):
        return day_of_year(self.year, self.month, self.day)

    def to_jd(self):
        return persian_to_jd(self.date)

    def add_days(self, delta):
        self.date = add_days(self.date, delta)
        self.year, self.month, self.day = self.date
        

# https://github.com/behrouzz/astrodata/raw/main/equinox/equinox_time.pickle
