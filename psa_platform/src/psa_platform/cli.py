"""Command-line smoke interface for Phase 1 provider connections."""

from __future__ import annotations

import argparse
import json
import os
from typing import Sequence

from .errors import PSAError
from .providers import CFTCClient, FREDClient, SECClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="psa", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="show configuration presence without values")

    fred = commands.add_parser("fred", help="fetch FRED observations")
    fred.add_argument("series_id")
    fred.add_argument("--limit", type=int, default=10)

    sec = commands.add_parser("sec", help="fetch public SEC EDGAR data")
    sec.add_argument("kind", choices=("submissions", "companyfacts"))
    sec.add_argument("cik")

    cftc = commands.add_parser("cftc", help="fetch filtered CFTC Legacy COT rows")
    cftc.add_argument("--report-type", choices=("FutOnly", "Combined"), required=True)
    cftc.add_argument("--market")
    cftc.add_argument("--limit", type=int, default=5)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "status":
            result = {
                "fred_api_key_configured": bool(os.getenv("PSA_FRED_API_KEY")),
                "sec_user_agent_configured": bool(os.getenv("PSA_SEC_USER_AGENT")),
                "cftc_credentials_required": False,
            }
        elif args.command == "fred":
            records = FREDClient().observations(args.series_id, limit=args.limit)
            result = [record.to_dict() for record in records]
        elif args.command == "sec":
            client = SECClient()
            payload = (
                client.submissions(args.cik)
                if args.kind == "submissions"
                else client.company_facts(args.cik)
            )
            result = payload.metadata()
        else:
            records = CFTCClient().legacy_positions(
                report_type=args.report_type,
                contract_market_name=args.market,
                limit=args.limit,
            )
            result = [record.to_dict() for record in records]
    except (PSAError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

