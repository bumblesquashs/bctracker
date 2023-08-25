
from datetime import timedelta

import helpers.date

from models.daterange import DateRange
from models.sheet import Sheet

def combine(system, services):
    '''Returns a list of sheets made from services with overlapping start/end dates'''
    if len(services) == 0:
        return []
    all_date_ranges = {s.schedule.date_range for s in services}
    all_start_dates = sorted({r.start for r in all_date_ranges})
    start_dates = set()
    for i, date in enumerate(all_start_dates):
        if i == 0 or helpers.date.days_between(all_start_dates[i - 1], date) > 7:
            start_dates.add(date)
    all_end_dates = sorted({r.end for r in all_date_ranges}, reverse=True)
    end_dates = set()
    for i, date in enumerate(all_end_dates):
        if i == 0 or helpers.date.days_between(date, all_end_dates[i - 1]) > 7:
            end_dates.add(date)
    end_dates.update({d - timedelta(days=1) for d in start_dates})
    start_dates.update({d + timedelta(days=1) for d in end_dates})
    dates = list(start_dates) + list(end_dates)
    sorted_dates = sorted(dates)[1:-1]
    i = iter(sorted_dates)
    
    sheets = []
    for (start_date, end_date) in zip(i, i):
        date_range = DateRange(start_date, end_date)
        date_range_services = {s.slice(date_range) for s in services if s.schedule.date_range.overlaps(date_range)}
        if len(date_range_services) == 0:
            continue
        if len(sheets) == 0:
            sheets.append(Sheet.combine(system, date_range_services))
        else:
            previous_sheet = sheets[-1]
            previous_services = {s for s in previous_sheet.services if not s.schedule.is_special}
            current_services = {s for s in date_range_services if not s.schedule.is_special}
            if previous_services.issubset(current_services) or current_services.issubset(previous_services):
                new_date_range = DateRange.combine([previous_sheet.schedule.date_range, date_range])
                new_services = {s.slice(new_date_range) for s in services if s.schedule.date_range.overlaps(new_date_range)}
                sheets[-1] = Sheet.combine(system, new_services)
            else:
                sheets.append(Sheet.combine(system, date_range_services))
    return sorted(sheets)
