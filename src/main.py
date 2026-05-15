from __future__ import annotations

import argparse

from src.simulation import HappyComputingSimulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Happy Computing simulation")
    parser.add_argument("--seed", type=int, default=12345, help="Random seed")
    parser.add_argument(
        "--workday-minutes",
        type=float,
        default=480,
        help="Length of the working day in minutes",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    simulation = HappyComputingSimulation(
        seed=args.seed,
        workday_minutes=args.workday_minutes,
    )
    results = simulation.run()

    print("Happy Computing - Simulación de una jornada")
    print(f"Seed: {simulation.seed}")
    print()
    print(f"Clientes generados: {results['clients_generated']}")
    print(f"Clientes completados: {results['clients_completed']}")
    print(f"Ganancia total: ${results['total_revenue']:.2f}")
    print(f"Tiempo final de simulación: {results['final_time']:.2f} minutos")
    print()
    print("Clientes completados por tipo:")
    print(f"Tipo 1: {results['completed_by_type'][1]}")
    print(f"Tipo 2: {results['completed_by_type'][2]}")
    print(f"Tipo 3: {results['completed_by_type'][3]}")
    print(f"Tipo 4: {results['completed_by_type'][4]}")
    print()
    print("Tiempos promedio de espera:")
    print(f"Vendedor: {results['average_seller_wait']:.2f} min")
    print(f"Reparación: {results['average_repair_wait']:.2f} min")
    print(f"Cambio de equipo: {results['average_change_wait']:.2f} min")
    print()
    print("Utilización de recursos:")
    print(f"Vendedores: {results['seller_utilization'] * 100:.2f}%")
    print(f"Técnicos: {results['technician_utilization'] * 100:.2f}%")
    print(f"Técnico especializado: {results['specialist_utilization'] * 100:.2f}%")


if __name__ == "__main__":
    main()
