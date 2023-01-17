import numpy as np
from persian import *
import jdatetime as jdt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_T(t):
    t0 = datetime(2000, 1, 1, 12)
    days = (t-t0).total_seconds()/86400
    return days / 36525


def mean_tropical_year(T):
    """
    Length of a tropical year in ephemeris days, between 8000 BC and 12000 AD

    Note: T is in Julian centuries of 36,525 days of 86,400 SI seconds,
    measured from noon January 1, 2000 TT.
    Ref: https://en.wikipedia.org/wiki/Tropical_year
    """
    return 365.2421896698 - 6.15359*1e-6*T - 7.29*1e-10*T**2 + 2.64*1e-10*T**3

from hypatie.coordinates import DECdms

def sun_mean_longtitude(T):
    # T = (JD - 2451545) / 36525
    return T

a = DECdms('+', d=280, m=27, s=59.2146)
b = a.deg
print(b)

# Newcomb & Laskar's expression chi hastan???

# https://en.wikipedia.org/wiki/VSOP_model
# https://cdsarc.cds.unistra.fr/ftp/cats/VI/81/ReadMe
# https://cdsarc.cds.unistra.fr/ftp/cats/VI/81/vsop87.txt
