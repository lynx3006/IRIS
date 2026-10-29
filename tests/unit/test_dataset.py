from pathlib import Path
from iris.monitoring.dataset import load_metrics

DATASET_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "rootcausebench"
    / "datasets"
    / "rootcausebench"
    / "checkout-latency-n-plus-one"
    / "environment"
    / "data"
    / "metrics.csv"
)

def test_load_metrics():
    observations = load_metrics(DATASET_PATH)

    assert len(observations) == 438
    assert observations[0].timestamp <= observations[-1].timestamp
    assert all(item.service for item in observations)
    assert all(item.metric for item in observations)
    assert all(isinstance(item.value, float) for item in observations)
