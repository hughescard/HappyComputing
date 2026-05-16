from __future__ import annotations

import csv
import statistics
from pathlib import Path

from src.simulation import HappyComputingSimulation


METRIC_NAMES = [
    "total_revenue",
    "clients_generated",
    "clients_completed",
    "final_time",
    "average_seller_wait",
    "average_repair_wait",
    "average_change_wait",
    "seller_utilization",
    "technician_utilization",
    "specialist_utilization",
    "completed_type_1",
    "completed_type_2",
    "completed_type_3",
    "completed_type_4",
    "revenue_type_1",
    "revenue_type_2",
    "revenue_type_3",
    "revenue_type_4",
]

CSV_FIELDNAMES = [
    "replication",
    "seed",
    "final_time",
    "workday_minutes",
    "total_revenue",
    "clients_generated",
    "clients_completed",
    "average_seller_wait",
    "average_repair_wait",
    "average_change_wait",
    "seller_utilization",
    "technician_utilization",
    "specialist_utilization",
    "completed_type_1",
    "completed_type_2",
    "completed_type_3",
    "completed_type_4",
    "revenue_type_1",
    "revenue_type_2",
    "revenue_type_3",
    "revenue_type_4",
]


def _flatten_replication_result(
    replication: int,
    seed: int,
    workday_minutes: float,
    result: dict,
) -> dict:
    completed_by_type = result["completed_by_type"]
    revenue_by_type = result["revenue_by_type"]

    return {
        "replication": replication,
        "seed": seed,
        "final_time": result["final_time"],
        "workday_minutes": workday_minutes,
        "total_revenue": result["total_revenue"],
        "clients_generated": result["clients_generated"],
        "clients_completed": result["clients_completed"],
        "average_seller_wait": result["average_seller_wait"],
        "average_repair_wait": result["average_repair_wait"],
        "average_change_wait": result["average_change_wait"],
        "seller_utilization": result["seller_utilization"],
        "technician_utilization": result["technician_utilization"],
        "specialist_utilization": result["specialist_utilization"],
        "completed_type_1": completed_by_type[1],
        "completed_type_2": completed_by_type[2],
        "completed_type_3": completed_by_type[3],
        "completed_type_4": completed_by_type[4],
        "revenue_type_1": revenue_by_type[1],
        "revenue_type_2": revenue_by_type[2],
        "revenue_type_3": revenue_by_type[3],
        "revenue_type_4": revenue_by_type[4],
    }


def _summarize_metric(results: list[dict], metric_name: str) -> dict:
    values = [row[metric_name] for row in results]
    if not values:
        return {"mean": 0.0, "min": 0.0, "max": 0.0, "stdev": 0.0}

    return {
        "mean": statistics.mean(values),
        "min": min(values),
        "max": max(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
    }


def _build_summary(results: list[dict]) -> dict:
    return {metric_name: _summarize_metric(results, metric_name) for metric_name in METRIC_NAMES}


def _write_csv(results: list[dict], output_csv: str) -> None:
    path = Path(output_csv)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)


def run_replications(
    replications: int,
    base_seed: int = 12345,
    workday_minutes: float = 480,
    output_csv: str | None = None,
) -> dict:
    if replications <= 0:
        raise ValueError("replications must be greater than 0")

    replication_results: list[dict] = []

    for replication in range(replications):
        seed = base_seed + replication
        simulation = HappyComputingSimulation(seed=seed, workday_minutes=workday_minutes)
        result = simulation.run()
        replication_results.append(
            _flatten_replication_result(replication, seed, workday_minutes, result)
        )

    if output_csv is not None:
        _write_csv(replication_results, output_csv)

    return {
        "replications": replications,
        "base_seed": base_seed,
        "workday_minutes": workday_minutes,
        "summary": _build_summary(replication_results),
        "replication_results": replication_results,
        "output_csv": output_csv,
    }
