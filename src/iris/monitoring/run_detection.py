from pathlib import Path
from iris.monitoring.dataset import load_metrics
from iris.monitoring.detector import StatisticalDetector
from iris.contracts import Signal
from iris.incidents.manager import IncidentManager

DATASET_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "rootcausebench"
    / "datasets"
    / "rootcausebench"
    / "checkout-latency-n-plus-one"
    / "environment"
    / "data"
    / "metrics.csv"
)

def main():
    observations = load_metrics(DATASET_PATH)
    detector = StatisticalDetector()

    anomalies = []
    incident_manager=IncidentManager()
    for observation in observations:
        result = detector.observe(observation)

        if result is not None and result.is_anomaly:
            anomalies.append(result)
            incident=incident_manager.process_signal(signal)
        signal = Signal(
        source="statistical_detector",
        service=observation.service,
        signal_type=observation.metric,
        observed_value=observation.value,
        detected_at=__import__("datetime").datetime.fromisoformat(
            observation.timestamp.replace("Z", "+00:00")
        ),
        description=(
            f"Z-score {result.z_score:.2f}; "
            f"baseline mean {result.baseline_mean:.2f}"
        ),
    )

    print(f"Total observations: {len(observations)}")
    print(f"Anomalies detected: {len(anomalies)}")
    print("\nFirst 15 anomalies:")

    for result in anomalies[:15]:
        observation = result.observation
        print(
            f"{observation.timestamp} | "
            f"{observation.service} | "
            f"{observation.metric} | "
            f"value={observation.value:.2f} | "
            f"z-score={result.z_score:.2f}"
        )
    print(f"\nIncidents created: {len(incident_manager.incidents)}")
    for incident in incident_manager.incidents:
        signals = incident_manager.incident_signals[incident.id]
        print(
            f"{incident.title} | "
            f"severity={incident.severity} | "
            f"status={incident.status} | "
            f"signals={len(signals)}"
        )    
if __name__ == "__main__":
    main()
