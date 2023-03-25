def today():
    from datetime import datetime as dt
    x = dt.now()
    x = x.replace(second=0, microsecond=0)
    return x

def deltaTime(min=1, sec=0):
    from datetime import timedelta as td
    return td(minutes=min, seconds=sec)

def futureTime(date=today(), min=1):
    return date + deltaTime(min)