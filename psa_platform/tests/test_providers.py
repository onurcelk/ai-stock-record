from datetime import datetime, timezone
from unittest import TestCase

from psa_platform.errors import ConfigurationError, ResponseValidationError
from psa_platform.models import FreshnessStatus
from psa_platform.providers.cftc import CFTCClient
from psa_platform.providers.fred import FREDClient
from psa_platform.providers.sec import SECClient, normalize_cik

NOW = datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc)


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get_json(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class NoWait:
    def wait(self) -> None:
        pass


class ProviderTests(TestCase):
    def test_fred_requires_local_key(self) -> None:
        with self.assertRaises(ConfigurationError):
            FREDClient(api_key="bad")

    def test_fred_normalizes_missing_values_without_invention(self) -> None:
        transport = FakeTransport(
            {"observations": [{"date": "2026-08-11", "value": "."}]}
        )
        records = FREDClient(
            api_key="a" * 32,
            transport=transport,
            clock=lambda: NOW,
        ).observations("DGS10")
        self.assertEqual(records[0].raw_value, ".")
        self.assertIsNone(records[0].adjusted_value)
        self.assertEqual(records[0].data_quality_score, 0.0)
        self.assertEqual(transport.calls[0]["params"]["api_key"], "a" * 32)

    def test_sec_identifies_the_application_and_pads_cik(self) -> None:
        transport = FakeTransport({"cik": "320193"})
        payload = SECClient(
            "PSA owner@example.com",
            transport=transport,
            clock=lambda: NOW,
            rate_limiter=NoWait(),
        ).submissions("CIK320193")
        call = transport.calls[0]
        self.assertEqual(call["path"], "/submissions/CIK0000320193.json")
        self.assertEqual(call["headers"]["User-Agent"], "PSA owner@example.com")
        self.assertEqual(payload.source, "SEC EDGAR")

    def test_sec_rejects_unidentified_client(self) -> None:
        with self.assertRaises(ConfigurationError):
            SECClient("anonymous")

    def test_normalize_cik_rejects_bad_input(self) -> None:
        self.assertEqual(normalize_cik(320193), "0000320193")
        with self.assertRaises(ValueError):
            normalize_cik("AAPL")

    def test_cftc_query_always_filters_report_type(self) -> None:
        transport = FakeTransport([])
        CFTCClient(transport=transport, clock=lambda: NOW).legacy_positions(
            report_type="FutOnly",
            contract_market_name="WHEAT-SRW",
        )
        where = transport.calls[0]["params"]["$where"]
        self.assertIn("futonly_or_combined='FutOnly'", where)
        self.assertIn("contract_market_name='WHEAT-SRW'", where)

    def test_cftc_rejects_cross_report_contamination(self) -> None:
        transport = FakeTransport(
            [
                {
                    "report_date_as_yyyy_mm_dd": "2026-08-04T00:00:00.000",
                    "contract_market_name": "WHEAT-SRW",
                    "futonly_or_combined": "Combined",
                }
            ]
        )
        with self.assertRaisesRegex(ResponseValidationError, "wrong report type"):
            CFTCClient(transport=transport, clock=lambda: NOW).legacy_positions(
                report_type="FutOnly"
            )

    def test_cftc_normalizes_numbers_and_marks_old_data_stale(self) -> None:
        transport = FakeTransport(
            [
                {
                    "id": "1",
                    "report_date_as_yyyy_mm_dd": "2026-07-01T00:00:00.000",
                    "contract_market_name": "WHEAT-SRW",
                    "market_and_exchange_names": "WHEAT-SRW - CBT",
                    "cftc_contract_market_code": "001602",
                    "commodity_name": "WHEAT",
                    "open_interest_all": "100",
                    "noncomm_positions_long_all": "60",
                    "noncomm_positions_short_all": "40",
                    "comm_positions_long_all": "30",
                    "comm_positions_short_all": "50",
                    "futonly_or_combined": "FutOnly",
                }
            ]
        )
        record = CFTCClient(transport=transport, clock=lambda: NOW).legacy_positions(
            report_type="FutOnly"
        )[0]
        self.assertEqual(record.adjusted_value, 20)
        self.assertEqual(record.raw_value["net_commercial"], -20)
        self.assertEqual(record.freshness_status, FreshnessStatus.STALE)
        self.assertEqual(record.data_quality_score, 1.0)

