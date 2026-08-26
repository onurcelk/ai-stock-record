"""FRED series-observation client."""

from __future__ import annotations

import os
import re
from datetime import date, datetime, time, timezone
from typing import Callable

from ..errors import ConfigurationError, ResponseValidationError
from ..http import JsonTransport, UrllibJsonTransport
from ..models import FreshnessStatus, Observation, VerificationResult, utc_now

FRED_BASE_URL = "https://api.stlouisfed.org"
FRED_ENDPOINT = "/fred/series/observations"
_SERIES_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


class FREDClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        transport: JsonTransport | None = None,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self.api_key = api_key or os.getenv("PSA_FRED_API_KEY", "")
        if not re.fullmatch(r"[a-z0-9]{32}", self.api_key):
            raise ConfigurationError(
                "Set PSA_FRED_API_KEY to the 32-character key from your FRED account"
            )
        self.transport = transport or UrllibJsonTransport()
        self.clock = clock

    def observations(
        self,
        series_id: str,
        *,
        observation_start: date | None = None,
        observation_end: date | None = None,
        limit: int = 100_000,
    ) -> list[Observation]:
        if not _SERIES_ID.fullmatch(series_id):
            raise ValueError("invalid FRED series_id")
        if not 1 <= limit <= 100_000:
            raise ValueError("limit must be between 1 and 100000")
        if observation_start and observation_end and observation_start > observation_end:
            raise ValueError("observation_start cannot be after observation_end")

        params: dict[str, str | int] = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "limit": limit,
        }
        if observation_start:
            params["observation_start"] = observation_start.isoformat()
        if observation_end:
            params["observation_end"] = observation_end.isoformat()

        payload = self.transport.get_json(
            base_url=FRED_BASE_URL,
            path=FRED_ENDPOINT,
            params=params,
        )
        if not isinstance(payload, dict) or not isinstance(payload.get("observations"), list):
            raise ResponseValidationError("FRED response has no observations list")

        retrieved_at = self.clock()
        results: list[Observation] = []
        for item in payload["observations"]:
            if not isinstance(item, dict) or not isinstance(item.get("date"), str):
                raise ResponseValidationError("FRED returned a malformed observation")
            try:
                observed_date = date.fromisoformat(item["date"])
            except ValueError:
                raise ResponseValidationError("FRED returned an invalid observation date") from None
            raw = item.get("value")
            adjusted = None
            if raw not in (None, "."):
                try:
                    adjusted = float(raw)
                except (TypeError, ValueError):
                    raise ResponseValidationError("FRED returned a non-numeric value") from None
            results.append(
                Observation(
                    symbol=series_id.upper(),
                    source="FRED",
                    observed_at=datetime.combine(observed_date, time.min, timezone.utc),
                    retrieved_at=retrieved_at,
                    freshness_status=FreshnessStatus.UNKNOWN,
                    raw_value=raw,
                    adjusted_value=adjusted,
                    data_quality_score=1.0 if adjusted is not None else 0.0,
                    verification_result=VerificationResult.UNVERIFIED,
                    endpoint_version="fred-v1:series_observations",
                    licensing_category="source_specific_review_required",
                )
            )
        return results

