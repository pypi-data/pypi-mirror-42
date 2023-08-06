__version__ = '0.1.7'
__all__ = ['Fdate', 'drange', 'today']


import datetime
from .fdate import Fdate


def drange(start, end, step=1):
    """ Iterates from start to end (both included).
    """
    d1 = Fdate(start)
    d2 = Fdate(end)
    delta = (d2 - d1) // step
    sign = 1 if delta >= 0 else - 1
    for i in range(abs(delta) + 1):
        yield Fdate(d1 + sign * i * step)


def today(shift=0):
    day = datetime.date.today() + datetime.timedelta(days=shift)
    return Fdate(day.strftime('%Y-%m-%d'))


