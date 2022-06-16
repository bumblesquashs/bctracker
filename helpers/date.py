
from datetime import timedelta

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
                date_strings.append(str(start_date))
            else:
                date_strings.append(str(start_date) + ' - ' + str(end_date))
            start_date = date
            end_date = None
        previous_date = date
    if end_date is None:
        date_strings.append(str(start_date))
    else:
        date_strings.append(str(start_date) + ' - ' + str(end_date))
    return ', '.join(date_strings)