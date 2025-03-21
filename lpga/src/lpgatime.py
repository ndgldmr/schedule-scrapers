import datetime
import pytz

def est_to_utc(est_datetime_str):
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')
    est_datetime = datetime.datetime.strptime(est_datetime_str, '%Y-%m-%d %H:%M:%S')
    est_datetime = est_timezone.localize(est_datetime, is_dst=None)
    utc_datetime = est_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

def convert_time(time_string):
    time_list = time_string.split()
    hour, minute = map(int, time_list[0].split(':'))
    period = time_list[1].upper()
    if period == 'P.M.' and hour != 12:
        hour += 12
    elif period == 'A.M.' and hour == 12:
        hour = 0
    return '{:02d}:{:02d}:00'.format(hour, minute)