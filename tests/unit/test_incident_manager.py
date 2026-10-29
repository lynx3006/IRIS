from datetime import datetime, timezone

from iris.contracts import Signal
from iris.incidents.manager import IncidentManager


def make_signal(service: str, minute: int) -> Signal:
    return Signal(
        source="statistical_detector",
        service=service,
        signal_type="http_server_duration_p99_ms",
        observed_value=3750.5,
        detected_at=datetime(
            2026, 6, 18, 15, minute, tzinfo=timezone.utc
        ),
    )


def test_same_service_signals_are_grouped():
    manager = IncidentManager(correlation_window_minutes=5)

    first = manager.process_signal(
        make_signal("checkoutservice", 3)
    )
    second = manager.process_signal(
        make_signal("checkoutservice", 5)
    )

    assert first.id == second.id
    assert len(manager.incidents) == 1
    assert len(manager.incident_signals[first.id]) == 2


def test_different_services_create_separate_incidents():
    manager = IncidentManager()

    first = manager.process_signal(
        make_signal("checkoutservice", 3)
    )
    second = manager.process_signal(
        make_signal("frontend", 4)
    )

    assert first.id != second.id
    assert len(manager.incidents) == 2


def test_signals_outside_window_create_separate_incidents():
    manager = IncidentManager(correlation_window_minutes=5)

    first = manager.process_signal(
        make_signal("checkoutservice", 3)
    )
    second = manager.process_signal(
        make_signal("checkoutservice", 10)
    )

    assert first.id != second.id
    assert len(manager.incidents) == 2

def test_closed_incident_is_not_reused():
    manager = IncidentManager()

    first = manager.process_signal(
        make_signal("checkoutservice", 3)
    )

    first.status = "closed"

    second = manager.process_signal(
        make_signal("checkoutservice", 4)
    )

    assert first.id != second.id
    assert len(manager.incidents) == 2