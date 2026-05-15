from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class EventType(Enum):
    ARRIVAL = auto()
    SELLER_SERVICE_END = auto()
    REPAIR_END = auto()
    EQUIPMENT_CHANGE_END = auto()


class ResourceType(Enum):
    SELLER = auto()
    TECHNICIAN = auto()
    SPECIALIST = auto()


@dataclass(order=True)
class Event:
    time: float
    priority: int
    event_type: EventType = field(compare=False)
    client_id: int | None = field(default=None, compare=False)
    resource_type: ResourceType | None = field(default=None, compare=False)
