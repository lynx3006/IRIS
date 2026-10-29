
from datetime import timedelta
from uuid import UUID
from iris.contracts import Incident, Signal

class IncidentManager:
    def __init__(self, correlation_window_minutes: int = 5):
        self.correlation_window = timedelta(
            minutes=correlation_window_minutes
        )
        self.incidents: list[Incident] = []
        self.incident_signals: dict[UUID, list[Signal]] = {}

    def process_signal(self, signal: Signal) -> Incident:
        for incident in self.incidents:
            if incident.status == "closed":
                continue

            signals = self.incident_signals[incident.id]
            latest_signal_time = max(item.detected_at for item in signals)
            if (
                signal.service == signals[0].service
                and signal.detected_at >= latest_signal_time
                and signal.detected_at - latest_signal_time
                <= self.correlation_window
            ):
                signals.append(signal)
                return incident

        incident = Incident(
            title=f"Anomalous behavior in {signal.service}",
            severity="medium",
        )
        self.incidents.append(incident)
        self.incident_signals[incident.id] = [signal]

        return incident