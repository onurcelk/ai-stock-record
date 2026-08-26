"""CFTC Legacy COT client with mandatory report-type filtering."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Callable, Literal

from ..errors import ResponseValidationError
from ..http import JsonTransport, UrllibJsonTransport
from ..models import (
    Observation,
    VerificationResult,
    classify_freshness,
    utc_now,
)

CFTC_BASE_URL = "https://publicreporting.cftc.gov"
CFTC_ENDPOINT = "/resource/srt6-5q2f.json"
ReportType = Literal["FutOnly", "Combined"]
_REPORT_TYPES = frozenset(("FutOnly", "Combined"))
_SELECT_FIELDS = (
    "id",
    "contract_market_name",
    "market_and_exchange_names",
    "report_date_as_yyyy_mm_dd",
    "cftc_contract_market_code",
    "commodity_name",
    "open_interest_all",
    "noncomm_positions_long_all",
    "noncomm_positions_short_all",
    "comm_positions_long_all",
    "comm_positions_short_all",
    "futonly_or_combined",
)
_NUMERIC_FIELDS = (
    "open_interest_all",
    "noncomm_positions_long_all",
    "noncomm_positions_short_all",
    "comm_positions_long_all",
    "comm_positions_short_all",
)


def _soql_literal(value: str) -> str:
    if not 1 <= len(value) <= 120 or any(ord(char) < 32 for char in value):
        raise ValueError("invalid CFTC market name")
    return "'" + value.replace("'", "''") + "'"


class CFTCClient:
    def __init__(
        self,
        *,
        transport: JsonTransport | None = None,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self.transport = transport or UrllibJsonTransport()
        self.clock = clock

    def legacy_positions(
        self,
        *,
        report_type: ReportType,
        contract_market_name: str | None = None,
        limit: int = 100,
    ) -> list[Observation]:
        if report_type not in _REPORT_TYPES:
            raise ValueError("report_type must be 'FutOnly' or 'Combined'")
        if not 1 <= limit <= 5_000:
            raise ValueError("limit must be between 1 and 5000")

        where = f"futonly_or_combined={_soql_literal(report_type)}"
        if contract_market_name:
            where += f" AND contract_market_name={_soql_literal(contract_market_name)}"
        payload = self.transport.get_json(
            base_url=CFTC_BASE_URL,
            path=CFTC_ENDPOINT,
            params={
                "$select": ",".join(_SELECT_FIELDS),
                "$where": where,
                "$order": "report_date_as_yyyy_mm_dd DESC",
                "$limit": limit,
            },
        )
        if not isinstance(payload, list):
            raise ResponseValidationError("CFTC response is not a list")

        retrieved_at = self.clock()
        return [self._normalize(row, report_type, retrieved_at) for row in payload]

    @staticmethod
    def _normalize(
        row: object,
        report_type: ReportType,
        retrieved_at: datetime,
    ) -> Observation:
        if not isinstance(row, dict):
            raise ResponseValidationError("CFTC returned a malformed row")
        if row.get("futonly_or_combined") != report_type:
            raise ResponseValidationError("CFTC returned a row from the wrong report type")
        try:
            observed_at = datetime.fromisoformat(str(row["report_date_as_yyyy_mm_dd"]))
            observed_at = observed_at.replace(tzinfo=timezone.utc)
            numeric = {field: int(row[field]) for field in _NUMERIC_FIELDS}
            market = str(row["contract_market_name"]).strip()
        except (KeyError, TypeError, ValueError):
            raise ResponseValidationError("CFTC row is missing a required value") from None
        if not market:
            raise ResponseValidationError("CFTC row has an empty market name")

        raw_value = {
            **numeric,
            "net_noncommercial": (
                numeric["noncomm_positions_long_all"]
                - numeric["noncomm_positions_short_all"]
            ),
            "net_commercial": (
                numeric["comm_positions_long_all"]
                - numeric["comm_positions_short_all"]
            ),
            "report_type": report_type,
            "commodity_name": row.get("commodity_name"),
            "market_and_exchange_names": row.get("market_and_exchange_names"),
            "cftc_contract_market_code": row.get("cftc_contract_market_code"),
        }
        present = sum(row.get(field) not in (None, "") for field in _SELECT_FIELDS)
        return Observation(
            symbol=market,
            source="CFTC COT Legacy",
            observed_at=observed_at,
            retrieved_at=retrieved_at,
            freshness_status=classify_freshness(
                observed_at,
                retrieved_at,
                maximum_age=timedelta(days=14),
            ),
            raw_value=raw_value,
            adjusted_value=raw_value["net_noncommercial"],
            data_quality_score=present / len(_SELECT_FIELDS),
            verification_result=VerificationResult.UNVERIFIED,
            endpoint_version="socrata:srt6-5q2f",
            licensing_category="US_government_public_data",
        )

