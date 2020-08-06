from datetime import datetime

def format_date(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    return date_object.strftime("%B %-d, %Y")

def format_time(time_string):
    (h, m, s) = time_string.split(':')
    if int(s) == 0:
        return h + ':' + m
    return time_string