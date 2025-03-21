import datetime
from datetime import timedelta
import pytz

# Converts the date-time string from ETC to UTC and returns the result.
def est_to_utc(est_datetime_str):
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')
    est_datetime = datetime.datetime.strptime(est_datetime_str, '%Y-%m-%d %H:%M:%S')
    est_datetime = est_timezone.localize(est_datetime, is_dst=None)
    utc_datetime = est_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Converts a time in HH:MM AM/PM format to it's corresponding 24-hour time in HH:MM:SS format.
def time24hour(time_12hour):
    time_12hour = time_12hour.upper()
    if not (time_12hour[-2:] == "AM" or time_12hour[-2:] == "PM") or len(time_12hour) < 6:
        return "Invalid input"
    hour, minute = map(int, time_12hour[:-2].split(":"))
    am_pm = time_12hour[-2:]
    if am_pm == 'PM' and hour != 12:
        hour += 12
    elif am_pm == 'AM' and hour == 12:
        hour = 0
    return f"{hour:02d}:{minute:02d}:00"

# Converts a date in 'Weekday, Month Day' format to 'YYYY-MM-DD' format.
def convert_date(input_date):
    current_year = datetime.datetime.now().year
    parsed_date = datetime.datetime.strptime(input_date, '%A, %b %d')
    parsed_date = parsed_date.replace(year=current_year)
    formatted_date = parsed_date.strftime('%Y-%m-%d')
    return formatted_date

# Subtracts 30 minutes from a date-time string in 'YYYY-MM DD HH:MM:SS' format.
def subtract_30_minutes(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time - timedelta(minutes=30)
    return new_date_time.strftime(date_format)

# Adds 210 minutes from a date-time string in 'YYYY-MM DD HH:MM:SS' format.
def add210minutes(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time + timedelta(minutes=210)
    return new_date_time.strftime(date_format)
