from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Client:
    id: int
    arrival_time: float
    service_type: int
    seller_service_start: float | None = None
    seller_service_end: float | None = None
    seller_sale_start: float | None = None
    seller_sale_end: float | None = None
    technical_queue_entry: float | None = None
    technical_service_start: float | None = None
    technical_service_end: float | None = None
    departure_time: float | None = None
