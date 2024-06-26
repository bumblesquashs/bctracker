
from di import di

from models.bus import Bus
from models.date import Date

from repositories import AgencyRepository, SystemRepository

class Transfer:
    '''Information about a bus moving from one system to another system'''
    
    __slots__ = (
        'id',
        'bus',
        'date',
        'old_system',
        'new_system'
    )
    
    @classmethod
    def from_db(cls, row, prefix='transfer', **kwargs):
        '''Returns a transfer initialized from the given database row'''
        agency_repository = kwargs.get('agency_repository') or di[AgencyRepository]
        system_repository = kwargs.get('system_repository') or di[SystemRepository]
        id = row[f'{prefix}_id']
        agency = agency_repository.find('bc-transit')
        bus = Bus.find(agency, row[f'{prefix}_bus_number'])
        old_system = system_repository.find(row[f'{prefix}_old_system_id'])
        new_system = system_repository.find(row[f'{prefix}_new_system_id'])
        date = Date.parse(row[f'{prefix}_date'], new_system.timezone)
        return cls(id, bus, date, old_system, new_system)
    
    def __init__(self, id, bus, date, old_system, new_system):
        self.id = id
        self.bus = bus
        self.date = date
        self.old_system = old_system
        self.new_system = new_system
