
from enum import Enum

class DownloadTrigger(Enum):
    WEEKLY = 'weekly'
    ADMIN = 'admin'
    LAUNCH_FLAG = 'launch_flag'
    NEAR_END_DATE = 'near_end_date'
    INVALID_POSITIONS = 'invalid_positions'
    MISSING = 'missing'
