
from .abc.backup import BackupService
from .abc.cron import CronService
from .abc.gtfs import GTFSService
from .abc.realtime import RealtimeService

backup: BackupService
cron: CronService
gtfs: GTFSService
realtime: RealtimeService
