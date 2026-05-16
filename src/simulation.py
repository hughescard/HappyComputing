from __future__ import annotations

import heapq
from collections import deque

from src.entities import Client
from src.events import Event, EventType, ResourceType
from src.random_generators import (
    RandomGenerator,
)


class HappyComputingSimulation:
    SERVICE_PRICES = {1: 0, 2: 350, 3: 500, 4: 750}

    def __init__(self, seed: int | None = None, workday_minutes: float = 480) -> None:
        self.seed = seed
        self.randoms = RandomGenerator(seed)
        self.clock = 0.0
        self.workday_minutes = workday_minutes
        self.event_calendar: list[Event] = []
        self.event_counter = 0
        self.clients: dict[int, Client] = {}
        self.queue_sellers = deque()
        self.queue_repairs = deque()
        self.queue_changes = deque()
        self.free_sellers = 2
        self.free_technicians = 3
        self.specialist_free = True

        self.total_revenue = 0.0
        self.clients_generated = 0
        self.clients_completed = 0
        self.completed_by_type = {1: 0, 2: 0, 3: 0, 4: 0}
        self.revenue_by_type = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
        self.total_seller_wait = 0.0
        self.total_repair_wait = 0.0
        self.total_change_wait = 0.0
        self.repair_clients_completed = 0
        self.change_clients_completed = 0
        self.busy_time_sellers = 0.0
        self.busy_time_technicians = 0.0
        self.busy_time_specialist = 0.0

    def schedule_event(
        self,
        time: float,
        event_type: EventType,
        client_id: int | None = None,
        resource_type: ResourceType | None = None,
    ) -> None:
        self.event_counter += 1
        event = Event(
            time=time,
            priority=self.event_counter,
            event_type=event_type,
            client_id=client_id,
            resource_type=resource_type,
        )
        heapq.heappush(self.event_calendar, event)

    def run(self) -> dict:
        first_arrival = self.randoms.time_between_arrivals()
        if first_arrival <= self.workday_minutes:
            self.schedule_event(first_arrival, EventType.ARRIVAL)

        while self.event_calendar:
            event = heapq.heappop(self.event_calendar)
            self.clock = event.time

            if event.event_type == EventType.ARRIVAL:
                self.process_arrival(event)
            elif event.event_type == EventType.SELLER_SERVICE_END:
                self.process_seller_service_end(event)
            elif event.event_type == EventType.SELLER_SALE_END:
                self.process_seller_sale_end(event)
            elif event.event_type == EventType.REPAIR_END:
                self.process_repair_end(event)
            elif event.event_type == EventType.EQUIPMENT_CHANGE_END:
                self.process_equipment_change_end(event)

        return self.build_results()

    def process_arrival(self, event: Event) -> None:
        self.clients_generated += 1
        client = Client(
            id=self.clients_generated,
            arrival_time=self.clock,
            service_type=self.randoms.service_type(),
        )
        self.clients[client.id] = client

        if self.free_sellers > 0:
            self.free_sellers -= 1
            client.seller_service_start = self.clock
            self.total_seller_wait += self.clock - client.arrival_time
            duration = self.randoms.seller_service_time()
            self.busy_time_sellers += duration
            self.schedule_event(
                self.clock + duration,
                EventType.SELLER_SERVICE_END,
                client_id=client.id,
                resource_type=ResourceType.SELLER,
            )
        else:
            self.queue_sellers.append(client.id)

        next_arrival = self.clock + self.randoms.time_between_arrivals()
        if next_arrival <= self.workday_minutes:
            self.schedule_event(next_arrival, EventType.ARRIVAL)

    def process_seller_service_end(self, event: Event) -> None:
        client = self.clients[event.client_id]
        client.seller_service_end = self.clock

        if client.service_type == 4:
            client.seller_sale_start = self.clock
            duration = self.randoms.seller_sale_time()
            self.busy_time_sellers += duration
            self.schedule_event(
                self.clock + duration,
                EventType.SELLER_SALE_END,
                client_id=client.id,
                resource_type=ResourceType.SELLER,
            )
            return

        self.free_sellers += 1

        if client.service_type in (1, 2):
            client.technical_queue_entry = self.clock
            self.queue_repairs.append(client.id)
            self.try_assign_repair()
        elif client.service_type == 3:
            client.technical_queue_entry = self.clock
            self.queue_changes.append(client.id)
            self.try_assign_specialist()

        self.try_assign_seller()

    def process_seller_sale_end(self, event: Event) -> None:
        client = self.clients[event.client_id]
        client.seller_sale_end = self.clock
        self.free_sellers += 1
        self.complete_client(client)
        self.try_assign_seller()

    def process_repair_end(self, event: Event) -> None:
        client = self.clients[event.client_id]
        client.technical_service_end = self.clock

        if event.resource_type == ResourceType.TECHNICIAN:
            self.free_technicians += 1
        elif event.resource_type == ResourceType.SPECIALIST:
            self.specialist_free = True

        self.complete_client(client)

        if event.resource_type == ResourceType.TECHNICIAN:
            self.try_assign_repair()
        elif event.resource_type == ResourceType.SPECIALIST:
            self.try_assign_specialist()

    def process_equipment_change_end(self, event: Event) -> None:
        client = self.clients[event.client_id]
        client.technical_service_end = self.clock
        self.specialist_free = True
        self.complete_client(client)
        self.try_assign_specialist()

    def try_assign_seller(self) -> None:
        while self.free_sellers > 0 and self.queue_sellers:
            client_id = self.queue_sellers.popleft()
            client = self.clients[client_id]
            self.free_sellers -= 1
            client.seller_service_start = self.clock
            self.total_seller_wait += self.clock - client.arrival_time
            duration = self.randoms.seller_service_time()
            self.busy_time_sellers += duration
            self.schedule_event(
                self.clock + duration,
                EventType.SELLER_SERVICE_END,
                client_id=client.id,
                resource_type=ResourceType.SELLER,
            )

    def try_assign_repair(self) -> None:
        while self.free_technicians > 0 and self.queue_repairs:
            client_id = self.queue_repairs.popleft()
            client = self.clients[client_id]
            self.free_technicians -= 1
            client.technical_service_start = self.clock
            if client.technical_queue_entry is not None:
                self.total_repair_wait += self.clock - client.technical_queue_entry
            duration = self.randoms.repair_time()
            self.busy_time_technicians += duration
            self.schedule_event(
                self.clock + duration,
                EventType.REPAIR_END,
                client_id=client.id,
                resource_type=ResourceType.TECHNICIAN,
            )

        # The specialist only helps with repairs if no change jobs are waiting.
        if self.specialist_free and not self.queue_changes and self.queue_repairs:
            client_id = self.queue_repairs.popleft()
            client = self.clients[client_id]
            self.specialist_free = False
            client.technical_service_start = self.clock
            if client.technical_queue_entry is not None:
                self.total_repair_wait += self.clock - client.technical_queue_entry
            duration = self.randoms.repair_time()
            self.busy_time_specialist += duration
            self.schedule_event(
                self.clock + duration,
                EventType.REPAIR_END,
                client_id=client.id,
                resource_type=ResourceType.SPECIALIST,
            )

    def try_assign_specialist(self) -> None:
        if not self.specialist_free:
            return

        if self.queue_changes:
            client_id = self.queue_changes.popleft()
            client = self.clients[client_id]
            self.specialist_free = False
            client.technical_service_start = self.clock
            if client.technical_queue_entry is not None:
                self.total_change_wait += self.clock - client.technical_queue_entry
            duration = self.randoms.equipment_change_time()
            self.busy_time_specialist += duration
            self.schedule_event(
                self.clock + duration,
                EventType.EQUIPMENT_CHANGE_END,
                client_id=client.id,
                resource_type=ResourceType.SPECIALIST,
            )
        elif self.queue_repairs:
            client_id = self.queue_repairs.popleft()
            client = self.clients[client_id]
            self.specialist_free = False
            client.technical_service_start = self.clock
            if client.technical_queue_entry is not None:
                self.total_repair_wait += self.clock - client.technical_queue_entry
            duration = self.randoms.repair_time()
            self.busy_time_specialist += duration
            self.schedule_event(
                self.clock + duration,
                EventType.REPAIR_END,
                client_id=client.id,
                resource_type=ResourceType.SPECIALIST,
            )

    def complete_client(self, client: Client) -> None:
        if client.departure_time is not None:
            return

        client.departure_time = self.clock
        price = self.SERVICE_PRICES[client.service_type]
        self.total_revenue += price
        self.revenue_by_type[client.service_type] += price
        self.clients_completed += 1
        self.completed_by_type[client.service_type] += 1

        if client.service_type in (1, 2):
            self.repair_clients_completed += 1
        elif client.service_type == 3:
            self.change_clients_completed += 1

    def build_results(self) -> dict:
        final_time = self.clock
        average_seller_wait = (
            self.total_seller_wait / self.clients_generated if self.clients_generated > 0 else 0.0
        )
        average_repair_wait = (
            self.total_repair_wait / self.repair_clients_completed
            if self.repair_clients_completed > 0
            else 0.0
        )
        average_change_wait = (
            self.total_change_wait / self.change_clients_completed
            if self.change_clients_completed > 0
            else 0.0
        )

        seller_utilization = (
            self.busy_time_sellers / (2 * final_time) if final_time > 0 else 0.0
        )
        technician_utilization = (
            self.busy_time_technicians / (3 * final_time) if final_time > 0 else 0.0
        )
        specialist_utilization = (
            self.busy_time_specialist / final_time if final_time > 0 else 0.0
        )

        return {
            "final_time": final_time,
            "workday_minutes": self.workday_minutes,
            "total_revenue": self.total_revenue,
            "clients_generated": self.clients_generated,
            "clients_completed": self.clients_completed,
            "completed_by_type": dict(self.completed_by_type),
            "revenue_by_type": dict(self.revenue_by_type),
            "average_seller_wait": average_seller_wait,
            "average_repair_wait": average_repair_wait,
            "average_change_wait": average_change_wait,
            "seller_utilization": seller_utilization,
            "technician_utilization": technician_utilization,
            "specialist_utilization": specialist_utilization,
            "pending_in_seller_queue": len(self.queue_sellers),
            "pending_in_repair_queue": len(self.queue_repairs),
            "pending_in_change_queue": len(self.queue_changes),
        }
