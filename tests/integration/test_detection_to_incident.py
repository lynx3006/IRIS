from datetime import datetime, timezone

from iris.contracts import Signal
from iris.incidents.manager import IncidentManager


def test_signals_from_detection_create_incidents():
    manager = IncidentManager()

    signal = Signal(
        source="statistical_detector",
        service="checkoutservice",
        signal_type="http_server_duration_p99_ms",
        observed_value=3750.5,
        detected_at=datetime(
            2026, 6, 18, 15, 3, tzinfo=timezone.utc
        ),
        description="Z-score 231.62",
    )

    incident = manager.process_signal(signal)

    assert incident.title == "Anomalous behavior in checkoutservice"
    assert incident.status == "open"
    assert len(manager.incident_signals[incident.id]) == 1