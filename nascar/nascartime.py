import datetime
from datetime import timedelta
import pytz

def split_date_time(input_datetime):
    input_datetime = input_datetime[:-1] + 'ST'
    datetime_obj = datetime.datetime.strptime(input_datetime, '%a, %b %d %I:%M %p %Z')
    datetime_obj = datetime_obj.replace(year=2023)
    date_str = datetime_obj.strftime('%Y-%m-%d')
    time_str = datetime_obj.strftime('%H:%M:%S')
    return date_str, time_str

def add3hours(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time + timedelta(hours=3)
    return new_date_time.strftime(date_format)

def utc(est_datetime_str):
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')
    est_datetime = datetime.datetime.strptime(est_datetime_str, '%Y-%m-%d %H:%M:%S')
    est_datetime = est_timezone.localize(est_datetime, is_dst=None)
    utc_datetime = est_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')