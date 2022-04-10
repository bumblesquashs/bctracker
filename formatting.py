from datetime import datetime, timedelta
import calendar

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

def flatten(dates):
    dates = sorted(dates)
    date_strings = []
    previous_date = dates[0]
    start_date = previous_date
    end_date = None
    for date in dates[1:]:
        if date == previous_date + timedelta(days=1):
            end_date = date
        else:
            if end_date is None:
                date_strings.append(long(start_date))
            else:
                date_strings.append(long(start_date) + ' - ' + long(end_date))
            start_date = date
            end_date = None
        previous_date = date
    if end_date is None:
        date_strings.append(long(start_date))
    else:
        date_strings.append(long(start_date) + ' - ' + long(end_date))
    return ', '.join(date_strings)
