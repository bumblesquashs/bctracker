
from models.sheet import Sheet

def combine(system, services):
    '''Returns a list of sheets made from services with overlapping start/end dates'''
    sheets = []
    cumulative_services = []
    for service in sorted(services, key=lambda s: s.schedule.start_date):
        if len(cumulative_services) == 0:
            cumulative_services.append(service)
        else:
            if service.schedule.start_date <= cumulative_services[-1].schedule.end_date:
                cumulative_services.append(service)
            else:
                sheets.append(Sheet.combine(system, cumulative_services))
                cumulative_services = [service]
    sheets.append(Sheet.combine(cumulative_services))
    return sorted(sheets)
