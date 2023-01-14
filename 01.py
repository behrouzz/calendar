from datetime import datetime, timedelta
import jdatetime as jdt

t0 = jdt.datetime(1360, 10, 11, 3, 19)
#t = jdt.datetime.now()
t = jdt.datetime(1401, 10, 11, 3, 19)

dt = t-t0

dt_secs = dt.total_seconds()
dt_days1 = dt_secs/86400
dt_days2 = dt.days

print('brith :', t0)
print('now   :', t)
print('delta :', dt)
print('secs  :', dt_secs)
print('days1 :', dt_days1)
print('days2 :', dt_days2)
print()

T0 = datetime(1982, 1, 1, 3, 19)
#T = datetime.now()
T = datetime(2023, 1, 1, 3, 19)

dT = T-T0

dT_secs = dT.total_seconds()
dT_days1 = dT_secs/86400
dT_days2 = dT.days

print('BIRTH :', T0)
print('NOW   :', T)
print('DELTA :', dT)
print('SECS  :', dT_secs)
print('DAYS1 :', dT_days1)
print('DAYS2 :', dT_days2)
