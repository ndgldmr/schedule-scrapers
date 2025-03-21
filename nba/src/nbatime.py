import pytz
import datetime
from datetime import timedelta

# Converts an EST date time string in YYYY-MM-DD HH:MM:SS format to it's corresponding UTC date time.
def utc(est_datetime_str):
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')
    est_datetime = datetime.datetime.strptime(est_datetime_str, '%Y-%m-%d %H:%M:%S')
    est_datetime = est_timezone.localize(est_datetime, is_dst=None)
    utc_datetime = est_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Converts a 12-hour time in HH:MM AM/PM format to it's corresponding 24-hour time in HH:MM:SS format.
def time24hour(time12hour):
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

# Converts a date in 'Weekday, Month Day' format to 'YYYY-MM-DD' format, where YYYY is the current year.
def format_date(date_string):
    now = datetime.datetime.now()
    year = now.year
    date = datetime.datetime.strptime(date_string, "%A, %B %d")
    date = date.replace(year=year)
    return date.strftime("%Y-%m-%d")

# Subtracts 30 minutes from a date time string in YYYY-MM-DD HH:MM:SS format.
def subtract30minutes(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time - timedelta(minutes=30)
    return new_date_time.strftime(date_format)

# Adds 210 minutes (3.5 hours) to a date time string in YYYY-MM-DD HH:MM:SS format.
def add210minutes(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time + timedelta(minutes=210)
    return new_date_time.strftime(date_format)

# A function for manual input
def manual():
    date = format_date(input('Enter the date: '))
    time = time24hour(input('Enter the time: '))
    dt = date + ' ' + time
    start_time = subtract30minutes(dt)
    end_time = add210minutes(start_time)
    start_time = utc(start_time)
    end_time = utc(end_time)
    print('Start Time (UTC): ' + start_time)
    print('End Time (UTC): ' + end_time)