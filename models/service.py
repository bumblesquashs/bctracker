
from enum import IntEnum

class ServiceType(IntEnum):
    WEEKDAY = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    WEEKDAY_EXCEPT_FRIDAY = 5
    FRI = 6
    WEEKEND = 7
    SAT = 8
    SUN = 9
    SPECIAL = 10
    UNKNOWN = 11

class Service:
    def __init__(self, system, service_id, mon, tue, wed, thu, fri, sat, sun):
        self.system = system
        self.service_id = service_id

        self.special_service = 'Special Service'

        if sat and sun:
            self.service_type = ServiceType.WEEKEND
        elif mon and tue and wed and thu and fri:
            self.service_type = ServiceType.WEEKDAY
        elif mon and tue and wed and thu and (not fri):
            self.service_type = ServiceType.WEEKDAY_EXCEPT_FRIDAY
        elif mon:
            self.service_type = ServiceType.MON
        elif tue:
            self.service_type = ServiceType.TUE
        elif wed:
            self.service_type = ServiceType.WED
        elif thu:
            self.service_type = ServiceType.THU
        elif fri:
            self.service_type = ServiceType.FRI
        elif sat:
            self.service_type = ServiceType.SAT
        elif sun:
            self.service_type = ServiceType.SUN
        elif not (mon or tue or wed or thu or fri or sat or sun):
            self.service_type = ServiceType.SPECIAL
        else:
            self.service_type = ServiceType.UNKNOWN
    
    def __str__(self):
        if self.service_type == ServiceType.WEEKDAY:
            return 'Weekdays'
        elif self.service_type == ServiceType.MON:
            return 'Mondays'
        elif self.service_type == ServiceType.TUE:
            return 'Tuesdays'
        elif self.service_type == ServiceType.WED:
            return 'Wednesdays'
        elif self.service_type == ServiceType.THU:
            return 'Thursdays'
        elif self.service_type == ServiceType.WEEKDAY_EXCEPT_FRIDAY:
            return 'Weekdays except Friday'
        elif self.service_type == ServiceType.FRI:
            return 'Fridays'
        elif self.service_type == ServiceType.WEEKEND:
            return 'Weekends'
        elif self.service_type == ServiceType.SAT:
            return 'Saturdays'
        elif self.service_type == ServiceType.SUN:
            return 'Sundays'
        elif self.service_type == ServiceType.SPECIAL:
            return f'Special: {self.special_service} Only'
        else:
            return 'Unknown'
    
    def __hash__(self):
        return hash(self.service_id)
    
    def __eq__(self, other):
        return self.service_id == other.service_id
    
    def __lt__(self, other):
        return self.service_type < other.service_type
