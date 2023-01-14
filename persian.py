# Add 1948319 to T.toordinal() to get julian date

from datetime import datetime

jd0 = 2451545 # datetime(2000, 1, 1, 12) = 2451545
JD0 = 1948319 # jdt.datetime(1378,10,11, 12) = 503226



def julien(T):
    """
    Julien date

    Argument:
    ---------
        T : jdatetime

    Return:
    -------
        jd : dulian date
    """
    return T.toordinal() + 1948319


def dt_to_jd(t):
    # faster than datetime_to_jd
    t0 = datetime(1858, 11, 17, 0)
    mjd = (t - t0).total_seconds()/86400
    jd = mjd + 2400000.5
    if t < datetime(1582,10,15):
        jd += 10
    return jd
