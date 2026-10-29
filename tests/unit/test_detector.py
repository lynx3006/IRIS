
from iris.monitoring.detector import (
    MetricObservation,
    StatisticalDetector,
)


def test_detector_flags_high_value():
    detector = StatisticalDetector(
        window_size=10,
        min_samples=5,
        z_threshold=3.0,
    )

    for value in [200, 210, 190, 205, 195]:
        result = detector.observe(
            MetricObservation(
                timestamp="2026-06-18T15:00:00Z",
                service="checkoutservice",
                metric="http_server_duration_p99_ms",
                value=value,
            )
        )
        assert result is None

    result = detector.observe(
        MetricObservation(
            timestamp="2026-06-18T15:03:00Z",
            service="checkoutservice",
            metric="http_server_duration_p99_ms",
            value=3750.5,
        )
    )

    assert result is not None
    assert result.is_anomaly is True
    assert result.z_score > 3.0


def test_services_have_separate_histories():
    detector = StatisticalDetector(min_samples=5)

    for value in [200, 210, 190, 205, 195]:
        detector.observe(
            MetricObservation(
                timestamp="2026-06-18T15:00:00Z",
                service="checkoutservice",
                metric="http_server_duration_p99_ms",
                value=value,
            )
        )

    result = detector.observe(
        MetricObservation(
            timestamp="2026-06-18T15:03:00Z",
            service="frontend",
            metric="http_server_duration_p99_ms",
            value=3750.5,
        )
    )

    # Frontend has no history yet, so it cannot be evaluated.
    assert result is None
