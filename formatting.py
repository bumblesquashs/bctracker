from datetime import datetime
import calendar

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

def days_since(date):
    now = datetime.now()
    years = now.year - date.year
    if date.month > now.month:
        years -= 1
        months = (now.month + 12) - date.month
    else:
        months = now.month - date.month
    if date.day > now.day:
        months -= 1
        days = (now.day + calendar.monthrange(now.year, now.month)[1]) - date.day
    else:
        days = now.day - date.day
    parts = []
    if years == 1:
        parts.append('1 year')
    elif years > 1:
        parts.append(f'{years} years')
    if months == 1:
        parts.append('1 month')
    elif months > 1:
        parts.append(f'{months} months')
    if days == 1:
        parts.append('1 day')
    elif days > 1 or len(parts) == 0:
        parts.append(f'{days} days')
    return ', '.join(parts) + ' ago'
    