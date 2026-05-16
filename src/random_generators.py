from __future__ import annotations

import random


class RandomGenerator:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def time_between_arrivals(self) -> float:
        return self.rng.expovariate(1 / 20)

    def service_type(self) -> int:
        u = self.rng.random()
        if u < 0.45:
            return 1
        if u < 0.70:
            return 2
        if u < 0.80:
            return 3
        return 4

    def seller_service_time(self) -> float:
        while True:
            value = self.rng.normalvariate(5, 2)
            if value > 0:
                return value

    def seller_sale_time(self) -> float:
        return self.seller_service_time()

    def repair_time(self) -> float:
        return self.rng.expovariate(1 / 20)

    def equipment_change_time(self) -> float:
        return self.rng.expovariate(1 / 15)
