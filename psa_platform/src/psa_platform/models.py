"""Shared, source-stamped data contracts used by every provider."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Any


class FreshnessStatus(StrEnum):
    FRESH = "fresh"
    STALE = "stale"
    LAST_KNOWN = "last_known"
    UNKNOWN = "unknown"


class VerificationResult(StrEnum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    FAILED = "failed"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _require_aware(value: datetime, field: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")


def classify_freshness(
    observed_at: datetime,
    retrieved_at: datetime,
    *,
    maximum_age: timedelta,
) -> FreshnessStatus:
    """Classify age without inventing a replacement for an old observation."""
    _require_aware(observed_at, "observed_at")
    _require_aware(retrieved_at, "retrieved_at")
    if maximum_age < timedelta(0):
        raise ValueError("maximum_age cannot be negative")
    return (
        FreshnessStatus.FRESH
        if retrieved_at - observed_at <= maximum_age
        else FreshnessStatus.STALE
    )


@dataclass(frozen=True, slots=True)
class Observation:
    """One normalized observation with provenance and quality metadata."""

    symbol: str
    source: str
    observed_at: datetime
    retrieved_at: datetime
    freshness_status: FreshnessStatus
    raw_value: Any
    adjusted_value: Any = None
    currency: str | None = None
    data_quality_score: float = 0.0
    verification_result: VerificationResult = VerificationResult.UNVERIFIED
    endpoint_version: str = ""
    licensing_category: str = "review_required"

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("symbol cannot be empty")
        if not self.source.strip():
            raise ValueError("source cannot be empty")
        _require_aware(self.observed_at, "observed_at")
        _require_aware(self.retrieved_at, "retrieved_at")
        if not 0.0 <= self.data_quality_score <= 1.0:
            raise ValueError("data_quality_score must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "source": self.source,
            "observed_at": self.observed_at.isoformat(),
            "retrieved_at": self.retrieved_at.isoformat(),
            "freshness_status": self.freshness_status.value,
            "raw_value": self.raw_value,
            "adjusted_value": self.adjusted_value,
            "currency": self.currency,
            "data_quality_score": self.data_quality_score,
            "verification_result": self.verification_result.value,
            "endpoint_version": self.endpoint_version,
            "licensing_category": self.licensing_category,
        }


@dataclass(frozen=True, slots=True)
class ProviderPayload:
    """Raw provider data accompanied by retrieval provenance.

    This is the Phase 1 boundary. Later normalization code can derive individual
    :class:`Observation` objects without losing which endpoint produced the data.
    """

    source: str
    endpoint: str
    endpoint_version: str
    retrieved_at: datetime
    licensing_category: str
    data: dict[str, Any] | list[Any]

    def __post_init__(self) -> None:
        _require_aware(self.retrieved_at, "retrieved_at")
        if not self.source or not self.endpoint.startswith("/"):
            raise ValueError("source and an absolute endpoint path are required")

    def metadata(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "endpoint": self.endpoint,
            "endpoint_version": self.endpoint_version,
            "retrieved_at": self.retrieved_at.isoformat(),
            "licensing_category": self.licensing_category,
            "payload_type": type(self.data).__name__,
            "record_count": len(self.data),
        }

