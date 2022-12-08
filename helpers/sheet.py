
from models.sheet import Sheet

def combine(system, services, include_special=False):
    '''Returns a list of sheets made from services with overlapping start/end dates'''
    sheets = []
    cumulative_services = []
    for service in sorted(services, key=lambda s: s.schedule.start_date):
        if len(cumulative_services) == 0:
            cumulative_services.append(service)
        else:
            end_date = max({s.schedule.end_date for s in cumulative_services})
            if service.schedule.start_date <= end_date:
                cumulative_services.append(service)
            else:
                sheets.append(Sheet.combine(system, cumulative_services, include_special))
                cumulative_services = [service]
    if len(cumulative_services) > 0:
        sheets.append(Sheet.combine(system, cumulative_services, include_special))
    return sorted(sheets)
