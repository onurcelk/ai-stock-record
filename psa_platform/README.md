# Personal Stock Analysis Platform

This directory contains the new PSA platform implementation. It is separate from the
closed research programme in `../Stock-Prediction-Models`.

## Current milestone

Phase 1 official-source ingestion is implemented for:

- FRED series observations (requires the owner's FRED API key)
- SEC EDGAR submissions and company facts (requires an identifying user agent)
- CFTC Legacy COT data (no credentials; report type is always filtered)

Every returned record or payload carries its source, retrieval time, endpoint version,
and licensing category. Missing values remain missing. No key or contact identity is
stored in source code.

## Local setup

Python 3.11 or newer is required. The package currently has no runtime dependencies.

```powershell
cd psa_platform
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
```

Set credentials only in the process environment or an operating-system credential
manager. Do not paste them into source files or commit a `.env` file.

```powershell
$env:PSA_FRED_API_KEY = "your-32-character-fred-key"
$env:PSA_SEC_USER_AGENT = "PersonalStockAnalysis owner@example.com"
```

`PSA_SEC_USER_AGENT` must contain a real application name and contact email belonging
to the operator. The client stays below the SEC's published ceiling of 10 requests per
second. Public SEC data retrieval does not require an EDGAR API token.

## Smoke commands

If the package is not installed, prefix commands in this directory with
`$env:PYTHONPATH = "src"`.

```powershell
python -m psa_platform status
python -m psa_platform fred DGS10 --limit 5
python -m psa_platform sec submissions 320193
python -m psa_platform sec companyfacts 320193
python -m psa_platform cftc --report-type FutOnly --market WHEAT-SRW --limit 1
```

The CFTC command requires `--report-type FutOnly` or `--report-type Combined`; the raw
`Legacy_All` dataset is never queried without that filter.

## Tests

The tests use only the standard library and never touch the network:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Official references

- [FRED series observations](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)
- [SEC EDGAR data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [SEC developer resources and fair-access limit](https://www.sec.gov/about/developer-resources)
- [CFTC Legacy_All dataset](https://publicreporting.cftc.gov/Commitments-of-Traders/Legacy_All/srt6-5q2f)

