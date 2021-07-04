import datetime
import matplotlib.pyplot as plt

log_paths = ('../logs/access_log.log', '../logs/access_log.log.2020-05-16')
#log_paths = ['/home/james/Documents/access_log.log']

access_counts = [0] * 366
raw_dates = []

def raw_date2daynum(date_str):
    date = datetime.datetime.strptime(date_str, "%d/%b/%Y")
    return date.timetuple().tm_yday

for log_path in log_paths:
    with open(log_path, 'r') as f:
        for line in f:
            date_str = line.rstrip().split(' ')[3] # date time string
            date_str = date_str[1:] #drop leading [
            raw_dates.append(date_str.split(':')[0]) # take only date

print('Total logs: {0}'.format(len(raw_dates)))
for date_str in raw_dates:
    access_counts[raw_date2daynum(date_str)] += 1
date_array = [raw_date2daynum(x) for x in raw_dates]
xvals = list(range(366))
plt.plot(xvals, access_counts)
plt.title('site accesses vs day of year')
plt.xlabel('day of year')
plt.xlim(min(date_array), max(date_array))
plt.ylabel('access counts')
plt.style.use('ggplot')
plt.show()
