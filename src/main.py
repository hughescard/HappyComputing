from __future__ import annotations

import argparse

from src.experiments import run_replications
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
    parser.add_argument(
        "--replications",
        type=int,
        default=None,
        help="Run multiple independent replications instead of a single simulation",
    )
    parser.add_argument(
        "--base-seed",
        type=int,
        default=12345,
        help="Base seed for replication runs",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Optional CSV path for replication results",
    )
    return parser.parse_args()


def print_single_results(simulation: HappyComputingSimulation, results: dict) -> None:
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


def print_replication_results(results: dict) -> None:
    summary = results["summary"]

    print("Happy Computing - Múltiples réplicas")
    print(f"Réplicas: {results['replications']}")
    print(f"Seed base: {results['base_seed']}")
    print(f"Jornada laboral: {results['workday_minutes']:.2f} minutos")
    print()
    print("Ganancia:")
    print(f"Promedio: ${summary['total_revenue']['mean']:.2f}")
    print(f"Mínimo: ${summary['total_revenue']['min']:.2f}")
    print(f"Máximo: ${summary['total_revenue']['max']:.2f}")
    print(f"Desviación estándar: ${summary['total_revenue']['stdev']:.2f}")
    print()
    print("Clientes:")
    print(f"Generados promedio: {summary['clients_generated']['mean']:.2f}")
    print(f"Completados promedio: {summary['clients_completed']['mean']:.2f}")
    print()
    print("Tiempos promedio de espera:")
    print(f"Vendedor: {summary['average_seller_wait']['mean']:.2f} min")
    print(f"Reparación: {summary['average_repair_wait']['mean']:.2f} min")
    print(f"Cambio de equipo: {summary['average_change_wait']['mean']:.2f} min")
    print()
    print("Utilización promedio de recursos:")
    print(f"Vendedores: {summary['seller_utilization']['mean'] * 100:.2f}%")
    print(f"Técnicos: {summary['technician_utilization']['mean'] * 100:.2f}%")
    print(f"Técnico especializado: {summary['specialist_utilization']['mean'] * 100:.2f}%")
    print()
    print("Clientes completados promedio por tipo:")
    print(f"Tipo 1: {summary['completed_type_1']['mean']:.2f}")
    print(f"Tipo 2: {summary['completed_type_2']['mean']:.2f}")
    print(f"Tipo 3: {summary['completed_type_3']['mean']:.2f}")
    print(f"Tipo 4: {summary['completed_type_4']['mean']:.2f}")

    output_csv = results.get("output_csv")
    if output_csv:
        print()
        print(f"Resultados individuales exportados a: {output_csv}")


def main() -> None:
    args = parse_args()
    if args.replications is not None:
        results = run_replications(
            replications=args.replications,
            base_seed=args.base_seed,
            workday_minutes=args.workday_minutes,
            output_csv=args.output_csv,
        )
        print_replication_results(results)
        return

    simulation = HappyComputingSimulation(
        seed=args.seed,
        workday_minutes=args.workday_minutes,
    )
    results = simulation.run()
    print_single_results(simulation, results)


if __name__ == "__main__":
    main()
