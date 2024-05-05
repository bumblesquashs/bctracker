
from __future__ import annotations

class RealtimeService:
    def update(self, system): pass
    def update_records(self): pass
    def get_last_updated(self, time_format) -> str | None: pass
    def validate(self, system) -> bool: pass
