
import re

def svg_string(name):
    '''Returns the SVG string for the given file name'''
    try:
        with open(f'./img/{name}.svg', 'r') as file:
            return file.read().replace('"', "\'")
    except:
        return ''

def key(number):
    '''Returns a sortable key based on numeric and non-numeric chars in a string'''
    return tuple([int(s) if s.isnumeric() else s for s in re.split('([0-9]+)', number)])

def flatten_dates(dates):
    '''Stringifies a list of dates with '-' between first and last consecutive dates and ',' between non-consecutive dates'''
    dates = sorted(dates)
    date_strings = []
    previous_date = dates[0]
    start_date = previous_date
    end_date = None
    for date in dates[1:]:
        if date == previous_date.next():
            end_date = date
        else:
            if end_date:
                date_strings.append(str(start_date) + ' - ' + str(end_date))
            else:
                date_strings.append(str(start_date))
            start_date = date
            end_date = None
        previous_date = date
    if end_date:
        date_strings.append(str(start_date) + ' - ' + str(end_date))
    else:
        date_strings.append(str(start_date))
    return ', '.join(date_strings)

def days_between(start_date, end_date):
    '''Returns the number of days between two given dates'''
    return (end_date.datetime - start_date.datetime).days
