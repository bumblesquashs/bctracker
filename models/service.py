
from datetime import datetime, timedelta

import formatting

class ServiceSchedule:
    __slots__ = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'indices', 'binary_string', 'special', 'name', 'included_dates', 'excluded_dates')
    
    def __init__(self, mon, tue, wed, thu, fri, sat, sun, included_dates=None, excluded_dates=None):
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun
        
        values = [mon, tue, wed, thu, fri, sat, sun]
        
        self.indices = [i for i, value in enumerate(values) if value]
        self.binary_string = ''.join(['1' if d else '0' for d in values])
        self.special = not (mon or tue or wed or thu or fri or sat or sun)
        
        if self.special:
            self.name = 'Special Service'
        elif mon and tue and wed and thu and fri and sat and sun:
            self.name = 'Every Day'
        elif mon and tue and wed and thu and fri and not (sat or sun):
            self.name = 'Weekdays'
        elif mon and not (tue or wed or thu or fri or sat or sun):
            self.name = 'Mondays'
        elif tue and not (mon or wed or thu or fri or sat or sun):
            self.name = 'Tuesdays'
        elif wed and not (mon or tue or thu or fri or sat or sun):
            self.name = 'Wednesdays'
        elif thu and not (mon or tue or wed or fri or sat or sun):
            self.name = 'Thursdays'
        elif fri and not (mon or tue or wed or thu or sat or sun):
            self.name = 'Fridays'
        elif sat and sun and not (mon or tue or wed or thu or fri):
            self.name = 'Weekends'
        elif sat and not (mon or tue or wed or thu or fri or sun):
            self.name = 'Saturdays'
        elif sun and not (mon or tue or wed or thu or fri or sat):
            self.name = 'Sundays'
        else:
            days = []
            if mon:
                days.append('Mon')
            if tue:
                days.append('Tue')
            if wed:
                days.append('Wed')
            if thu:
                days.append('Thu')
            if fri:
                days.append('Fri')
            if sat:
                days.append('Sat')
            if sun:
                days.append('Sun')
            self.name = '/'.join(days)
        
        self.included_dates = set() if included_dates is None else included_dates
        self.excluded_dates = set() if excluded_dates is None else excluded_dates
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        if self.special:
            return hash(self.included_dates_string)
        return hash(self.binary_string)
    
    def __eq__(self, other):
        if self.special and other.special:
            return self.included_dates == other.included_dates
        return self.binary_string == other.binary_string
    
    def __lt__(self, other):
        if self.special and other.special and len(self.included_dates) > 0 and len(other.included_dates) > 0:
            return sorted(self.included_dates)[0] < sorted(other.included_dates)[0]
        return self.binary_string > other.binary_string
    
    @property
    def mon_status(self):
        return self.get_status(self.mon, 0)
    
    @property
    def tue_status(self):
        return self.get_status(self.tue, 1)
    
    @property
    def wed_status(self):
        return self.get_status(self.wed, 2)
    
    @property
    def thu_status(self):
        return self.get_status(self.thu, 3)
    
    @property
    def fri_status(self):
        return self.get_status(self.fri, 4)
    
    @property
    def sat_status(self):
        return self.get_status(self.sat, 5)
    
    @property
    def sun_status(self):
        return self.get_status(self.sun, 6)
    
    @property
    def included_dates_string(self):
        return formatting.flatten(self.included_dates)
    
    @property
    def excluded_dates_string(self):
        return formatting.flatten(self.excluded_dates)
    
    def includes(self, date):
        if date in self.included_dates:
            return True
        if date in self.excluded_dates:
            return False
        return date.weekday() in self.indices
    
    def get_status(self, active, weekday):
        included_count = len([d for d in self.included_dates if d.weekday() == weekday])
        excluded_count = len([d for d in self.excluded_dates if d.weekday() == weekday])
        if active or included_count > 3:
            if excluded_count > 3:
                return 'limited'
            return 'running'
        if included_count > 0:
            return 'limited'
        return 'not-running'

class Service:
    __slots__ = ('system', 'id', 'start_date', 'end_date', 'schedule')
    
    def __init__(self, system, row):
        self.system = system
        self.id = row['service_id']
        self.start_date = formatting.csv(row['start_date']).date()
        self.end_date = formatting.csv(row['end_date']).date()
        
        mon = row['monday'] == '1'
        tue = row['tuesday'] == '1'
        wed = row['wednesday'] == '1'
        thu = row['thursday'] == '1'
        fri = row['friday'] == '1'
        sat = row['saturday'] == '1'
        sun = row['sunday'] == '1'
        
        delta = self.end_date - self.start_date
        if mon and tue and wed and thu and fri and sat and sun and delta.days < 7:
            included_dates = [self.start_date + timedelta(days=i) for i in range(delta.days + 1)]
            self.schedule = ServiceSchedule(False, False, False, False, False, False, False, included_dates)
        else:
            self.schedule = ServiceSchedule(mon, tue, wed, thu, fri, sat, sun)
    
    def __str__(self):
        if self.schedule.special:
            return self.schedule.included_dates_string
        start = formatting.long(self.start_date)
        end = formatting.long(self.end_date)
        return f'{start} to {end}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        self.schedule < other.schedule
    
    @property
    def is_current(self):
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        return self.start_date <= date <= self.end_date
    
    @property
    def is_today(self):
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        if date < self.start_date or date > self.end_date:
            return False
        return self.schedule.includes(date)
    
    def include(self, date):
        self.schedule.included_dates.add(date.date())
    
    def exclude(self, date):
        self.schedule.excluded_dates.add(date.date())

class ServiceGroup:
    __slots__ = ('services', 'start_date', 'end_date', 'schedule')
    
    def __init__(self, services, schedule):
        self.services = services
        
        if len(services) == 0:
            self.start_date = None
            self.end_date = None
        else:
            self.start_date = min({s.start_date for s in services})
            self.end_date = max({s.end_date for s in services})
        
        self.schedule = schedule
    
    def __str__(self):
        return f'{self.schedule} ({self.date_string})'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return self.start_date == other.start_date and self.end_date == other.end_date and self.schedule == other.schedule
    
    def __lt__(self, other):
        if self.start_date == other.start_date:
            return self.schedule < other.schedule
        return self.start_date < other.start_date
    
    @property
    def date_string(self):
        if self.schedule.special:
            return self.schedule.included_dates_string
        start = formatting.long(self.start_date)
        end = formatting.long(self.end_date)
        return f'{start} to {end}'
    
    @property
    def is_current(self):
        if self.start_date is None or self.end_date is None:
            return False
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        return self.start_date <= date <= self.end_date
    
    @property
    def is_today(self):
        if self.start_date is None or self.end_date is None:
            return False
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        if date < self.start_date or date > self.end_date:
            return False
        return self.schedule.includes(date)

def create_service_group(services):
    indices = {i for s in services for i in s.schedule.indices}
    mon = 0 in indices
    tue = 1 in indices
    wed = 2 in indices
    thu = 3 in indices
    fri = 4 in indices
    sat = 5 in indices
    sun = 6 in indices
    included_dates = {d for s in services for d in s.schedule.included_dates}
    excluded_dates = {d for s in services for d in s.schedule.excluded_dates}
    schedule = ServiceSchedule(mon, tue, wed, thu, fri, sat, sun, {d for d in included_dates if d not in excluded_dates}, {d for d in excluded_dates if d not in included_dates})
    return ServiceGroup(services, schedule)
