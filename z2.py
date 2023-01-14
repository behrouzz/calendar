from persian import *

today = (1401, 10, 24)
date2 = (1378,10,11) # = datetime(2000, 1, 1) = 2451544.5
date1 = (-5334, 9, 2)

a = days_between_dates(date1, today)
a = a + 0.5 # at 0h
#print(a)

#JD0 = 1948319 # jdt.datetime(1378,10,11, 12) = 503226


#print(persian_to_jd(date2))

b = get_period(1401)
