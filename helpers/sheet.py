
from datetime import timedelta

from models.daterange import DateRange
from models.sheet import Sheet

def combine(system, services):
    '''Returns a list of sheets made from services with overlapping start/end dates'''
    if len(services) == 0:
        return []
    all_date_ranges = {s.schedule.date_range for s in services}
    start_dates = {r.start for r in all_date_ranges}
    end_dates = {r.end for r in all_date_ranges}
    all_start_dates = start_dates.union({d + timedelta(days=1) for d in end_dates})
    all_end_dates = end_dates.union({d - timedelta(days=1) for d in start_dates})
    dates = list(all_start_dates) + list(all_end_dates)
    sorted_dates = sorted(dates)[1:-1]
    i = iter(sorted_dates)
    
    sheets = []
    for (start_date, end_date) in zip(i, i):
        date_range = DateRange(start_date, end_date)
        date_range_services = {s for s in services if s.schedule.date_range.overlaps(date_range)}
        if len(date_range_services) == 0:
            continue
        if len(sheets) == 0:
            sheets.append(Sheet.combine(system, date_range_services, date_range))
        else:
            previous_sheet = sheets[-1]
            previous_services = {s for s in previous_sheet.services if not s.schedule.is_special}
            current_services = {s for s in date_range_services if not s.schedule.is_special}
            if previous_services.issubset(current_services) or current_services.issubset(previous_services):
                date_range = DateRange.combine([previous_sheet.schedule.date_range, date_range])
                new_services = {s for s in services if s.schedule.date_range.overlaps(date_range)}
                sheets[-1] = Sheet.combine(system, new_services, date_range)
            else:
                sheets.append(Sheet.combine(system, date_range_services, date_range))
    return sorted(sheets)
