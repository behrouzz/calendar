from persian import *

m = matrix_days(1403)
doy = day_of_year(1403, 1, 5)

lps = leaps_between_two_years(1400,1408)
days = days_between_years(1400,1408)


date1 = (1400, 1, 1)
date2 = (1400, 1, 2)

dd = days_between_dates(date1, date2)
a = add_days(date1, 366)


b = jd_to_persian(2451544.5)
print(b)
