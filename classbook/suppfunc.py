from .models import Days
import datetime
from datetime import timedelta


def make_year():
    one_day = timedelta(days=1)
    start_year = datetime.datetime(2022, 9, 1)
    for day in range(365-90):
        c_date = start_year+one_day*day
        if not Days.objects.filter(date=c_date):
            _ = Days()
            _.date = c_date
            _.save()


def make_schedule():
    pass
