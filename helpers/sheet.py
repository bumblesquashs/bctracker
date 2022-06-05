
from models.sheet import Sheet

def combine(services):
    sheets = []
    for service in sorted(services, key=lambda s: s.start_date):
        added = False
        for sheet in sheets:
            if service.start_date <= sheet.end_date and service.end_date >= sheet.start_date:
                sheet.add_service(service)
                added = True
        if not added:
            sheets.append(Sheet(service))
    return sorted(sheets)
