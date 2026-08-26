from datetime import datetime, timedelta, timezone
from unittest import TestCase

from psa_platform.models import (
    FreshnessStatus,
    Observation,
    classify_freshness,
)


class ObservationTests(TestCase):
    def test_quality_score_must_be_bounded(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 0 and 1"):
            Observation(
                symbol="DGS10",
                source="FRED",
                observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                retrieved_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
                freshness_status=FreshnessStatus.FRESH,
                raw_value="4.1",
                data_quality_score=1.1,
            )

    def test_freshness_classification_is_deterministic(self) -> None:
        observed = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.assertEqual(
            classify_freshness(
                observed,
                observed + timedelta(days=7),
                maximum_age=timedelta(days=7),
            ),
            FreshnessStatus.FRESH,
        )
        self.assertEqual(
            classify_freshness(
                observed,
                observed + timedelta(days=8),
                maximum_age=timedelta(days=7),
            ),
            FreshnessStatus.STALE,
        )

