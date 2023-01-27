import numpy as np
#from .data import periods, official_leaps
from.birashk import add_days


class Persian:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.date = (year, month, day)

    def __repr__(self):
        return 'Persian'+str((self.year, self.month, self.day))


    #def __add__(self, new):

    def add_days(self, delta):
        self.date = add_days(self.date, delta)
        self.year, self.month, self.day = self.date
        

##    @classmethod
##    def persian(cls, year, month, day):
##        return cls(year, month, day)

