from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.simulation import HappyComputingSimulation


def print_result(title, result):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    for key, value in result.items():
        print(f"{key}: {value}")


def check_revenue_consistency(result):
    completed = result["completed_by_type"]

    expected_revenue = (
        completed[1] * 0
        + completed[2] * 350
        + completed[3] * 500
        + completed[4] * 750
    )

    assert result["total_revenue"] == expected_revenue, (
        f"Revenue mismatch. Expected {expected_revenue}, "
        f"got {result['total_revenue']}"
    )


def check_basic_invariants(result):
    assert result["clients_completed"] <= result["clients_generated"]
    assert result["total_revenue"] >= 0
    assert result["final_time"] >= 0

    assert 0 <= result["seller_utilization"] <= 1
    assert 0 <= result["technician_utilization"] <= 1
    assert 0 <= result["specialist_utilization"] <= 1

    assert result["pending_in_seller_queue"] == 0
    assert result["pending_in_repair_queue"] == 0
    assert result["pending_in_change_queue"] == 0

    check_revenue_consistency(result)


def test_normal_day():
    sim = HappyComputingSimulation(seed=12345)
    result = sim.run()

    check_basic_invariants(result)
    print_result("TEST 1 - Jornada normal con seed fija", result)


def test_very_short_day():
    sim = HappyComputingSimulation(seed=12345, workday_minutes=1)
    result = sim.run()

    check_basic_invariants(result)
    print_result("TEST 2 - Jornada muy corta", result)


def test_no_clients_day():
    sim = HappyComputingSimulation(seed=12345, workday_minutes=0)
    result = sim.run()

    assert result["clients_generated"] == 0
    assert result["clients_completed"] == 0
    assert result["total_revenue"] == 0
    assert result["final_time"] == 0

    print_result("TEST 3 - Jornada sin clientes", result)


def test_many_seller_queue_clients():
    sim = HappyComputingSimulation(seed=12345, workday_minutes=30)

    # Forzamos muchas llegadas rápidas.
    sim.randoms.time_between_arrivals = lambda: 0.5

    # Forzamos que todos sean venta de equipo reparado.
    # Así solo pasan por vendedor y podemos probar cola de vendedores.
    sim.randoms.service_type = lambda: 4

    # Forzamos atención de vendedor relativamente lenta.
    sim.randoms.seller_service_time = lambda: 5

    result = sim.run()

    check_basic_invariants(result)

    assert result["clients_generated"] > 2
    assert result["average_seller_wait"] > 0

    print_result("TEST 4 - Cola de vendedores forzada", result)


def test_repair_queue_pressure():
    sim = HappyComputingSimulation(seed=12345, workday_minutes=30)

    # Muchas llegadas rápidas.
    sim.randoms.time_between_arrivals = lambda: 0.5

    # Todos piden reparación fuera de garantía.
    sim.randoms.service_type = lambda: 2

    # Vendedor rápido para que muchos lleguen a reparación.
    sim.randoms.seller_service_time = lambda: 0.1

    # Reparación lenta para formar cola técnica.
    sim.randoms.repair_time = lambda: 20

    result = sim.run()

    check_basic_invariants(result)

    assert result["clients_generated"] > 3
    assert result["completed_by_type"][2] == result["clients_completed"]
    assert result["average_repair_wait"] > 0
    assert result["total_revenue"] == result["clients_completed"] * 350

    print_result("TEST 5 - Presión sobre cola de reparaciones", result)


def test_specialist_change_queue_pressure():
    sim = HappyComputingSimulation(seed=12345, workday_minutes=30)

    # Muchas llegadas rápidas.
    sim.randoms.time_between_arrivals = lambda: 0.5

    # Todos piden cambio de equipo.
    sim.randoms.service_type = lambda: 3

    # Vendedor rápido.
    sim.randoms.seller_service_time = lambda: 0.1

    # Cambio lento para formar cola del técnico especializado.
    sim.randoms.equipment_change_time = lambda: 20

    result = sim.run()

    check_basic_invariants(result)

    assert result["clients_generated"] > 1
    assert result["completed_by_type"][3] == result["clients_completed"]
    assert result["average_change_wait"] > 0
    assert result["total_revenue"] == result["clients_completed"] * 500

    print_result("TEST 6 - Presión sobre técnico especializado", result)


def run_all_checks():
    test_normal_day()
    test_very_short_day()
    test_no_clients_day()
    test_many_seller_queue_clients()
    test_repair_queue_pressure()
    test_specialist_change_queue_pressure()

    print("\nTodas las pruebas manuales terminaron correctamente.")


if __name__ == "__main__":
    run_all_checks()
