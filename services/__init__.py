
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .impl.backup import BackupService
    from .impl.cron import CronService
    from .impl.gtfs import GTFSService
    from .impl.realtime import RealtimeService

backup: BackupService
cron: CronService
gtfs: GTFSService
realtime: RealtimeService
