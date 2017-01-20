def first_day_current_month():
    from datetime import date, datetime
    today = datetime.today()
    return date(year=today.year, month=today.month, day=1)

def last_day_current_month():
    from datetime import date, datetime
    from calendar import monthrange
    today = datetime.today()
    last_day = monthrange(today.year, today.month)[1]
    return date(year=today.year, month=today.month, day=last_day)
