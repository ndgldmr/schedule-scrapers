import datetime
from datetime import timedelta
import pytz

# Converts a date in 'Weekday, Month Day' format to 'YYYY-MM-DD' format, where YYYY is the current year.
def yyyy_mm_dd(date_string) -> str:
    now = datetime.datetime.now()
    year = now.year
    date = datetime.datetime.strptime(date_string, "%A %b %d")
    date = date.replace(year=year)
    return date.strftime("%Y-%m-%d")

# Converts a 12-hour time in 'HH:MM AM/PM' format to it's corresponding 24-hour time in 'HH:MM:SS' format.
def time_24hour(time12hour) -> str:
    time12hour = time12hour[:-3].upper()
    if not (time12hour[-2:] == "AM" or time12hour[-2:] == "PM") or len(time12hour) < 6:
        return "Invalid input"
    hour, minute = map(int, time12hour[:-2].split(":"))
    am_pm = time12hour[-2:]
    if am_pm == 'PM' and hour != 12:
        hour += 12
    elif am_pm == 'AM' and hour == 12:
        hour = 0
    return f"{hour:02d}:{minute:02d}:00"

# Subtracts 30 minutes from the date-time input string and returns the result.
def subtract_30minutes(date_string) -> str:
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time - timedelta(minutes=30)
    return new_date_time.strftime(date_format)

# Adds 4 hours to the date-time input string and returns the result.
def add_4hours(date_string) -> str:
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time + timedelta(hours=4)
    return new_date_time.strftime(date_format)

# Converts the date-time string from ETC to UTC and returns the result.
def est_to_utc(est_datetime_str) -> str:
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')
    est_datetime = datetime.datetime.strptime(est_datetime_str, '%Y-%m-%d %H:%M:%S')
    est_datetime = est_timezone.localize(est_datetime, is_dst=None)
    utc_datetime = est_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
