"""Public SEC EDGAR submissions and XBRL clients."""

from __future__ import annotations

import os
import re
import threading
import time
from datetime import datetime
from typing import Callable

from ..errors import ConfigurationError, ResponseValidationError
from ..http import JsonTransport, UrllibJsonTransport
from ..models import ProviderPayload, utc_now

SEC_BASE_URL = "https://data.sec.gov"
_CONTACT_EMAIL = re.compile(r"^[^\s]+\s+[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_cik(cik: str | int) -> str:
    value = str(cik).strip()
    if value.upper().startswith("CIK"):
        value = value[3:]
    if not value.isdigit() or len(value) > 10:
        raise ValueError("CIK must contain at most 10 digits")
    return value.zfill(10)


class _RateLimiter:
    """Per-process limiter kept below the SEC's 10 requests/second ceiling."""

    def __init__(self, requests_per_second: float = 8.0) -> None:
        self.minimum_interval = 1.0 / requests_per_second
        self._last_request = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            remaining = self.minimum_interval - (now - self._last_request)
            if remaining > 0:
                time.sleep(remaining)
            self._last_request = time.monotonic()


class SECClient:
    def __init__(
        self,
        user_agent: str | None = None,
        *,
        transport: JsonTransport | None = None,
        clock: Callable[[], datetime] = utc_now,
        rate_limiter: _RateLimiter | None = None,
    ) -> None:
        self.user_agent = user_agent or os.getenv("PSA_SEC_USER_AGENT", "")
        if not _CONTACT_EMAIL.fullmatch(self.user_agent):
            raise ConfigurationError(
                "Set PSA_SEC_USER_AGENT to 'ApplicationName contact@example.com'"
            )
        self.transport = transport or UrllibJsonTransport()
        self.clock = clock
        self.rate_limiter = rate_limiter or _RateLimiter()

    def submissions(self, cik: str | int) -> ProviderPayload:
        padded = normalize_cik(cik)
        return self._get(f"/submissions/CIK{padded}.json", "edgar-submissions-v1")

    def company_facts(self, cik: str | int) -> ProviderPayload:
        padded = normalize_cik(cik)
        return self._get(
            f"/api/xbrl/companyfacts/CIK{padded}.json",
            "edgar-xbrl-companyfacts-v1",
        )

    def frame(self, taxonomy: str, concept: str, unit: str, period: str) -> ProviderPayload:
        for label, value in {
            "taxonomy": taxonomy,
            "concept": concept,
            "unit": unit,
            "period": period,
        }.items():
            if not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", value):
                raise ValueError(f"invalid SEC frame {label}")
        path = f"/api/xbrl/frames/{taxonomy}/{concept}/{unit}/{period}.json"
        return self._get(path, "edgar-xbrl-frames-v1")

    def _get(self, path: str, endpoint_version: str) -> ProviderPayload:
        self.rate_limiter.wait()
        payload = self.transport.get_json(
            base_url=SEC_BASE_URL,
            path=path,
            headers={
                "User-Agent": self.user_agent,
                "Accept-Encoding": "identity",
            },
        )
        if not isinstance(payload, (dict, list)):
            raise ResponseValidationError("SEC returned an invalid payload")
        return ProviderPayload(
            source="SEC EDGAR",
            endpoint=path,
            endpoint_version=endpoint_version,
            retrieved_at=self.clock(),
            licensing_category="US_government_public_data",
            data=payload,
        )

