from percal import Persian, from_jd

d = Persian(1401, 11, 8)
jd = d.to_jd()
print(jd)


date = from_jd(jd)
print(date)
