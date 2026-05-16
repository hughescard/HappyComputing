from __future__ import annotations

import math


class LinearCongruentialGenerator:
    """Generador Park-Miller MINSTD para uniformes pseudoaleatorios en (0, 1)."""

    MODULUS = 2_147_483_647
    MULTIPLIER = 16_807

    def __init__(self, seed: int | None = None) -> None:
        if seed is None:
            seed = 12345

        seed = int(seed) % self.MODULUS
        if seed <= 0:
            seed += 1

        self.state = seed

    def next_int(self) -> int:
        self.state = (self.MULTIPLIER * self.state) % self.MODULUS
        return self.state

    def uniform(self) -> float:
        return self.next_int() / self.MODULUS


class RandomGenerator:
    """Genera todas las variables aleatorias del modelo a partir de un LCG propio."""

    def __init__(self, seed: int | None = None) -> None:
        self.lcg = LinearCongruentialGenerator(seed)
        self._has_cached_normal = False
        self._cached_normal = 0.0

    def uniform(self) -> float:
        return self.lcg.uniform()

    def exponential(self, mean: float) -> float:
        """Genera una exponencial usando transformada inversa."""
        if mean <= 0:
            raise ValueError("mean must be greater than 0")

        return -mean * math.log(self.uniform())

    def normal(self, mean: float, std_dev: float) -> float:
        """Genera una normal usando el método de Box-Muller."""
        if std_dev <= 0:
            raise ValueError("std_dev must be greater than 0")

        if self._has_cached_normal:
            self._has_cached_normal = False
            return mean + std_dev * self._cached_normal

        u1 = self.uniform()
        u2 = self.uniform()
        radius = math.sqrt(-2 * math.log(u1))
        angle = 2 * math.pi * u2
        z0 = radius * math.cos(angle)
        z1 = radius * math.sin(angle)

        self._cached_normal = z1
        self._has_cached_normal = True

        return mean + std_dev * z0

    def time_between_arrivals(self) -> float:
        return self.exponential(mean=20)

    def service_type(self) -> int:
        # Variable discreta generada por probabilidades acumuladas.
        u = self.uniform()
        if u < 0.45:
            return 1
        if u < 0.70:
            return 2
        if u < 0.80:
            return 3
        return 4

    def seller_service_time(self) -> float:
        while True:
            value = self.normal(mean=5, std_dev=2)
            if value > 0:
                return value

    def seller_sale_time(self) -> float:
        return self.seller_service_time()

    def repair_time(self) -> float:
        return self.exponential(mean=20)

    def equipment_change_time(self) -> float:
        return self.exponential(mean=15)
