
import pytest
from pydantic import ValidationError
from iris.contracts import Incident, Signal

def test_signal_accepts_valid_data():
    signal = Signal(
        source="metrics",
        service="payment-api",
        signal_type="high_cpu",
        observed_value=95.0,
        description="CPU usage exceeded normal levels",
    )

    assert signal.service == "payment-api"
    assert signal.observed_value == 95.0
    assert signal.description == "CPU usage exceeded normal levels"

def test_signal_rejects_empty_source():
    with pytest.raises(ValidationError):
        Signal(
            source="",
            service="payment-api",
            signal_type="high_cpu",
            observed_value=95.0,
        )

def test_incident_defaults():
    incident = Incident(
        title="Payment API is unavailable",
        severity="high",
    )

    assert incident.status == "open"
    assert incident.id is not None
    assert incident.created_at is not None


def test_incident_rejects_invalid_severity():
    with pytest.raises(ValidationError):
        Incident(
            title="Payment API is unavailable",
            severity="critical",
        )


def test_incidents_get_unique_ids():
    first = Incident(title="Incident A", severity="low")
    second = Incident(title="Incident B", severity="low")

    assert first.id != second.id
