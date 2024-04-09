
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
