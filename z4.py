from persian import *
import jdatetime as jdt
from datetime import datetime, timedelta

def is_official_leap(year):
    r = year % 33
    kabiseh = False
    
    if (year>=1244) and (year<=1342):
        if r in [1,5,9,13,17,21,26,30]:
            kabiseh = True
    elif (year>=1343) and (year<=1472):
        if r in [1,5,9,13,17,22,26,30]:
            kabiseh = True
    else:
        raise Exception('Valid years: from 1244 to 1472')
    return kabiseh


for y in range(1244, 1473):
    if is_official_leap(y):
        print(y)

"""
To be read:
- article of Mousa Akrami
- wikipedia: Mean tropical year
- wikipedian: گاه‌شماری هجری خورشیدی حسابی
- some article in downloads folder
"""
