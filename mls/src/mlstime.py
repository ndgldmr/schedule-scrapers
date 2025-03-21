import datetime
from datetime import timedelta
import pytz

# Converts the date-time string from ETC to UTC and returns the result.
def utc(est_datetime_str):
    if 'TBD' in est_datetime_str:
        return est_datetime_str
    est_timezone = pytz.timezone('US/Eastern')
    utc_timezone = pytz.timezone('UTC')
    est_datetime = datetime.datetime.strptime(est_datetime_str, '%Y-%m-%d %H:%M:%S')
    est_datetime = est_timezone.localize(est_datetime, is_dst=None)
    utc_datetime = est_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Converts a time in HH:MM AM/PM format to it's corresponding 24-hour time in HH:MM:SS format.
def time24hour(time_12hour):
    if 'TBD' in time_12hour:
        return time_12hour
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

# Converts a date in 'Weekday, Month Day' format to 'YYYY-MM-DD' format, where YYYY is the current year.
def format_date(date_string):
    now = datetime.datetime.now()
    year = now.year
    date = datetime.datetime.strptime(date_string, "%A, %B %d")
    date = date.replace(year=year)
    return date.strftime("%Y-%m-%d")

# Subtracts 30 minutes from the date-time input string and returns the result.
def subtract30minutes(date_string):
    if 'TBD' in date_string:
        return date_string
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time - timedelta(minutes = 30)
    return new_date_time.strftime(date_format)

# Adds 210 minutes to the date-time input string and returns the result.
def add210minutes(date_string):
    if 'TBD' in date_string:
        return date_string
    date_format = '%Y-%m-%d %H:%M:%S'
    date_time = datetime.datetime.strptime(date_string, date_format)
    new_date_time = date_time + timedelta(minutes = 210)
    return new_date_time.strftime(date_format)

# Converts a date in 'M/DD' format to it's corresponding 'YYYY-MM-DD' format.
def convert_date(date):
    month, day = date.split('/')
    month = month.zfill(2)
    day = day.zfill(2)
    output_date = f"2023-{month}-{day}"
    return output_date

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