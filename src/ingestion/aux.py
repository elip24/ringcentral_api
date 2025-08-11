import calendar
from datetime import datetime, timedelta, time, date, timezone


def get_last_date_of_month(first_time:datetime):
    last_day_of_month=calendar.monthrange(first_time.year, first_time.month)[1]
    last_day_of_month=date(first_time.year,first_time.month,last_day_of_month)
    last_time_of_month=datetime.combine(last_day_of_month,time.max,tzinfo=timezone.utc)
    return last_time_of_month

def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield y, m+1
