
import csv
from pathlib import Path
from iris.monitoring.detector import MetricObservation

def load_metrics(path: str | Path) -> list[MetricObservation]:
    observations = []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            observations.append(
                MetricObservation(
                    timestamp=row["timestamp"],
                    service=row["service"],
                    metric=row["metric"],
                    value=float(row["value"]),
                )
            )

    observations.sort(key=lambda item: item.timestamp)
    return observations