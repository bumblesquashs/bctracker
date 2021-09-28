from datetime import datetime

def format_csv(date_string):
    return datetime.strptime(date_string, "%Y%m%d")

def format_date(date):
    if isinstance(date, str):
        date_object = datetime.strptime(date, "%Y-%m-%d")
    else:
        date_object = date
    return date_object.strftime("%B %-d, %Y")

def format_date_mobile(date):
    if isinstance(date, str):
        date_object = datetime.strptime(date, "%Y-%m-%d")
    else:
        date_object = date
    if date_object.year == datetime.now().year:
        return date_object.strftime("%b %-d")
    else:
        return date_object.strftime("%b %-d, %Y")

def format_time(time_string):
    if time_string.count(':') < 2:
        return time_string
    (h, m, s) = time_string.split(':')
    if int(s) == 0:
        return h + ':' + m
    return time_string

def get_minutes(hours, minutes):
    return ((hours * 60) + minutes) % 1440 # For times past midnight

'''
Returns the time as a string in HH:mm from two times, also
strings in HH:mm format.
'''
def duration_between_timestrs(start_time, end_time):
    end_min = int(end_time[0:2]) * 60 + int(end_time[3:5])
    start_min = int(start_time[0:2]) * 60 + int(start_time[3:5])
    diff = abs(end_min - start_min)
    return "{0:02d}:{1:02d}".format(diff // 60, diff % 60)

