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
    (h, m, s) = time_string.split(':')
    if int(s) == 0:
        return h + ':' + m
    return time_string