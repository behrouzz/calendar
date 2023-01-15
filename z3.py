from persian import *
import jdatetime as jdt
from datetime import datetime, timedelta

date = (1401, 12, 29)
y, m, d = date

for delta in range(1, 1000):
    kh = add_days(date, delta)
    ks = str(kh).replace('(','').replace(')','').split(',')
    ks = [i.strip() for i in ks]
    ks = [ks[0], ks[1].zfill(2), ks[2].zfill(2)]
    ks = '-'.join(ks)

    yaru = jdt.datetime(y,m,d) +timedelta(days=delta)

    print(delta)
    print(ks)
    print(yaru.isoformat()[:10])
    print('-'*20)
