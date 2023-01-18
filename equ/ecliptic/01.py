from vernal_ecliptic import *

ver_et, ver_jd, ver_cal = get_equinox(year=2023,
                                      month=3,
                                      day=20,
                                      delta_days=1,
                                      steps=10000)

print(ver_et)
print(ver_jd)
print(ver_cal)
