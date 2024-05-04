
import re

from models.daterange import DateRange
from models.sheet import Sheet

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

def combine_sheets(system, services):
    '''Returns a list of sheets made from services with overlapping start/end dates'''
    if not services:
        return []
    all_date_ranges = {s.schedule.date_range for s in services}
    start_dates = {r.start for r in all_date_ranges}
    end_dates = {r.end for r in all_date_ranges}
    all_start_dates = start_dates.union({d.next() for d in end_dates})
    all_end_dates = end_dates.union({d.previous() for d in start_dates})
    dates = list(all_start_dates) + list(all_end_dates)
    sorted_dates = sorted(dates)[1:-1]
    i = iter(sorted_dates)
    
    sheets = []
    for (start_date, end_date) in zip(i, i):
        date_range = DateRange(start_date, end_date)
        date_range_services = {s for s in services if s.schedule.date_range.overlaps(date_range)}
        if not date_range_services:
            continue
        if sheets:
            previous_sheet = sheets[-1]
            previous_services = {s for s in previous_sheet.services if not s.schedule.is_special}
            current_services = {s for s in date_range_services if not s.schedule.is_special}
            if previous_services.issubset(current_services) or current_services.issubset(previous_services):
                date_range = DateRange.combine([previous_sheet.schedule.date_range, date_range])
                new_services = {s for s in services if s.schedule.date_range.overlaps(date_range)}
                sheets[-1] = Sheet(system, new_services, date_range)
            else:
                sheets.append(Sheet(system, date_range_services, date_range))
        else:
            sheets.append(Sheet(system, date_range_services, date_range))
    final_sheets = []
    for sheet in sheets:
        if final_sheets:
            previous_sheet = final_sheets[-1]
            if len(previous_sheet.schedule.date_range) <= 7 or len(sheet.schedule.date_range) <= 7:
                date_range = DateRange.combine([previous_sheet.schedule.date_range, sheet.schedule.date_range])
                combined_services = previous_sheet.services.union(sheet.services)
                final_sheets[-1] = Sheet(system, combined_services, date_range)
            else:
                final_sheets.append(sheet)
        else:
            final_sheets.append(sheet)
    return final_sheets
