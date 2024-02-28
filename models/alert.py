
from enum import Enum

import helpers.system

class Alert:
    
    __slots__ = (
        'system',
        'id',
        'active_periods',
        'cause',
        'effect',
        'severity',
        'title',
        'description'
    )
    
    @classmethod
    def from_db(cls, row, prefix='alert'):
        system = helpers.system.find(row[f'{prefix}_system_id'])
        id = row[f'{prefix}_id']
        active_periods = row[f'{prefix}_active_periods']
        try:
            cause = AlertCause[row[f'{prefix}_cause']]
        except:
            cause = AlertCause.UNKNOWN_CAUSE
        try:
            effect = AlertEffect[row[f'{prefix}_effect']]
        except:
            effect = AlertEffect.UNKNOWN_EFFECT
        try:
            severity = AlertSeverity[row[f'{prefix}_severity']]
        except:
            severity = AlertSeverity.UNKNOWN_SEVERITY
        title = row[f'{prefix}_title']
        description = row[f'{prefix}_description']
        return cls(system, id, active_periods, cause, effect, severity, title, description)
    
    def __init__(self, system, id, active_periods, cause, effect, severity, title, description):
        self.system = system
        self.id = id
        self.active_periods = active_periods
        self.cause = cause
        self.effect = effect
        self.severity = severity
        self.title = title
        self.description = description
    
    def __str__(self):
        if self.title:
            return self.title
        if self.effect and self.effect.is_known:
            return str(self.effect)
        return 'Details unavailable'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
class AlertTarget:
    
    __slots__ = (
        'system',
        'alert_id',
        'route_id',
        'stop_id',
        'trip_id'
    )
    
    @classmethod
    def from_db(cls, row, prefix='alert_target'):
        system = helpers.system.find(row[f'{prefix}_system_id'])
        alert_id = row[f'{prefix}_alert_id']
        route_id = row[f'{prefix}_route_id']
        stop_id = row[f'{prefix}_stop_id']
        trip_id = row[f'{prefix}_trip_id']
        return cls(system, alert_id, route_id, stop_id, trip_id)
    
    @property
    def route(self):
        if self.route_id is None:
            return None
        return self.system.get_route(route_id=self.route_id)
    
    @property
    def stop(self):
        if self.stop_id is None:
            return None
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def trip(self):
        if self.trip_id is None:
            return None
        return self.system.get_trip(self.trip_id)
    
    def __init__(self, system, alert_id, route_id, stop_id, trip_id):
        self.system = system
        self.alert_id = alert_id
        self.route_id = route_id
        self.stop_id = stop_id
        self.trip_id = trip_id
    
    def __hash__(self):
        return hash((self.route_id, self.stop_id, self.trip_id))
    
    def __eq__(self, other):
        return self.route_id == other.route_id and self.stop_id == other.stop_id and self.trip_id == other.trip_id

class AlertCause(Enum):
    UNKNOWN_CAUSE = 'Unknown Cause'
    OTHER_CAUSE = 'Other Cause'
    TECHNICAL_PROBLEM = 'Technical Problem'
    STRIKE = 'Strike'
    DEMONSTRATION = 'Demonstration'
    ACCIDENT = 'Accident'
    HOLIDAY = 'Holiday'
    WEATHER = 'Weather'
    MAINTENANCE = 'Maintenance'
    CONSTRUCTION = 'Construction'
    POLICE_ACTIVITY = 'Police Activity'
    MEDICAL_EMERGENCY = 'Medical Emergency'
    
    @property
    def is_known(self):
        return self != AlertCause.UNKNOWN_CAUSE
    
    def __str__(self):
        return self.value

class AlertEffect(Enum):
    NO_SERVICE = 'No Service'
    REDUCED_SERVICE = 'Reduced Service'
    SIGNIFICANT_DELAYS = 'Significant Delays'
    DETOUR = 'Detour'
    ADDITIONAL_SERVICE = 'Additional Service'
    MODIFIED_SERVICE = 'Modified Service'
    OTHER_EFFECT = 'Other Effect'
    UNKNOWN_EFFECT = 'Unknown Effect'
    STOP_MOVED = 'Stop Moved'
    NO_EFFECT = 'No Effect'
    ACCESSIBILITY_ISSUE = 'Accessibility Issue'
    
    @property
    def is_known(self):
        return self != AlertEffect.UNKNOWN_EFFECT
    
    def __str__(self):
        return self.value

class AlertSeverity(Enum):
    UNKNOWN_SEVERITY = 'Unknown Severity'
    INFO = 'Info'
    WARNING = 'Warning'
    SEVERE = 'Severe'
    
    @property
    def is_known(self):
        return self != AlertSeverity.UNKNOWN_SEVERITY
    
    def __str__(self):
        return self.value
