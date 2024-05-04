
from __future__ import annotations

class BackupService:
    def run(self, date, include_db, delete_files): pass

class CronService:
    def start(self): pass
    def stop(self): pass
    def handle_gtfs(self): pass
    def handle_realtime(self): pass

class GTFSService:
    def load(self, system, force_download, update_db): pass
    def download(self, system): pass
    def update_database(self, system): pass
    def validate(self, system) -> bool: pass
    def update_cache_in_background(self, system): pass

class RealtimeService:
    def update(self, system): pass
    def update_records(self): pass
    def get_last_updated(self, time_format) -> str | None: pass
    def validate(self, system) -> bool: pass
