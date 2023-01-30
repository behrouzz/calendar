import numpy as np
from .birashk import add_days as bir_add_days
from .birashk import is_leapyear as bir_is_leapyear
from .birashk import day_of_year as bir_day_of_year
from .birashk import jd_to_persian, persian_to_jd
from .gregorian import add_days as gre_add_days
from .gregorian import greg_leap as gre_is_leapyear
from .gregorian import day_of_year as gre_day_of_year
from .gregorian import jd_to_gregorian, gregorian_to_jd


def et2jd(et):
    J2000 = 2451545.0
    return J2000 + (et / 86400)


def persian_from_jd(jd):
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
        return bir_is_leapyear(self.year)

    def day_of_year(self):
        return bir_day_of_year(self.year, self.month, self.day)

    def to_jd(self):
        return persian_to_jd(self.date)

    def to_gregorian(self):
        jd = self.to_jd()
        return gregorian_from_jd(jd)

    def add_days(self, delta):
        self.date = bir_add_days(self.date, delta)
        self.year, self.month, self.day = self.date
        


def gregorian_from_jd(jd):
    y,m,d = jd_to_gregorian(jd)
    return Gregorian(y,m,d)


class Gregorian:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.date = (year, month, day)

    def __repr__(self):
        return 'Gregorian'+str((self.year, self.month, self.day))

    def is_leap(self):
        return gre_is_leapyear(self.year)

    def day_of_year(self):
        return gre_day_of_year(self.year, self.month, self.day)

    def to_jd(self):
        return gregorian_to_jd(self.date)

    def to_persian(self):
        jd = self.to_jd()
        return persian_from_jd(jd)

    def add_days(self, delta):
        self.date = gre_add_days(self.date, delta)
        self.year, self.month, self.day = self.date


# https://github.com/behrouzz/astrodata/raw/main/equinox/equinox_time.pickle
