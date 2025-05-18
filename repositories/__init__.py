
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .impl.adornment import AdornmentRepository
    from .impl.agency import AgencyRepository
    from .impl.assignment import AssignmentRepository
    from .impl.departure import DepartureRepository
    from .impl.model import ModelRepository
    from .impl.order import OrderRepository
    from .impl.overview import OverviewRepository
    from .impl.point import PointRepository
    from .impl.position import PositionRepository
    from .impl.record import RecordRepository
    from .impl.region import RegionRepository
    from .impl.route import RouteRepository
    from .impl.stop import StopRepository
    from .impl.system import SystemRepository
    from .impl.theme import ThemeRepository
    from .impl.transfer import TransferRepository
    from .impl.trip import TripRepository

adornment: AdornmentRepository
agency: AgencyRepository
assignment: AssignmentRepository
departure: DepartureRepository
model: ModelRepository
order: OrderRepository
overview: OverviewRepository
point: PointRepository
position: PositionRepository
record: RecordRepository
region: RegionRepository
route: RouteRepository
stop: StopRepository
system: SystemRepository
theme: ThemeRepository
transfer: TransferRepository
trip: TripRepository
