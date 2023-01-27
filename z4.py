from persian import *


date = (1400, 1, 3)
delta = -367
official = True



y,m,d = date

y_days = 366 if is_leapyear(y, official) else 365

day = day_of_year(y, m, d, official)

#mat = matrix_days(y, official)[:day] # HAZF SHAVAD

n = 0
new_y = y


mat = matrix_days(y, official)[:day]

while n < abs(delta):
    print(1)
    new_y -= 1
    new_mat = matrix_days(new_y, official)
    n = len(mat) + len(new_mat)
    if n > abs(delta):
        result = np.vstack((new_mat, mat))[delta-1]
        #break
    else:
        mat = np.vstack((new_mat, mat))
#result = (new_y, mat[-1, 1], mat[-1, 2])
#print(result)

