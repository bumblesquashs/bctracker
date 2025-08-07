
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .impl.agency import AgencyRepository
    from .impl.allocation import AllocationRepository
    from .impl.assignment import AssignmentRepository
    from .impl.decoration import DecorationRepository
    from .impl.departure import DepartureRepository
    from .impl.livery import LiveryRepository
    from .impl.model import ModelRepository
    from .impl.order import OrderRepository
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

agency: AgencyRepository
allocation: AllocationRepository
assignment: AssignmentRepository
decoration: DecorationRepository
departure: DepartureRepository
livery: LiveryRepository
model: ModelRepository
order: OrderRepository
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
