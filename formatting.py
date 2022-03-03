from datetime import datetime

def csv(date):
    if isinstance(date, str):
        return datetime.strptime(date, '%Y%m%d')
    return date.strftime('%Y%m%d')

def database(date):
    if isinstance(date, str):
        return datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%Y-%m-%d')

def long(date):
    if date.year == datetime.now().year:
        return date.strftime('%B %-d')
    return date.strftime('%B %-d, %Y')

def short(date):
    if date.year == datetime.now().year:
        return date.strftime("%b %-d")
    return date.strftime("%b %-d, %Y")
