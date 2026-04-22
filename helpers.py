
import re

from random import randint, seed
from colorsys import hls_to_rgb

from models.context import Context

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

def generate_colour(context: Context, number):
    '''Generate a random colour based on context and route number'''
    if context.default_route_colour:
        return context.default_route_colour
    seed(context.system_id)
    number_digits = ''.join([d for d in number if d.isdigit()])
    if len(number_digits) == 0:
        h = randint(1, 360) / 360.0
    else:
        h = (randint(1, 360) + (int(number_digits) * 137.508)) / 360.0
    seed(context.system_id + number)
    l = randint(30, 50) / 100.0
    s = randint(50, 100) / 100.0
    rgb = hls_to_rgb(h, l, s)
    r = int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    return f'{r:02x}{g:02x}{b:02x}'

def generate_text_colour(colour):
    r = int(colour[0:1], 16)
    g = int(colour[2:3], 16)
    b = int(colour[5:6], 16)
    luminance = ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255
    if luminance > 0.5:
        return '000000'
    return 'FFFFFF'
