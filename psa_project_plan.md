# Personal Stock Analysis Platform Project Plan

The controlling roadmap is `PSA platform roadmap update`. This file is a short execution
index; it replaces the earlier, unrelated Product Strategy Analytics placeholder.

## Phase 1 — Free official sources (in progress)

- [x] Define source-stamped data contracts.
- [x] Implement credential-safe HTTPS JSON transport.
- [x] Implement and live-verify filtered CFTC Legacy COT retrieval.
- [x] Implement SEC submissions, company-facts, and frames clients.
- [x] Implement FRED series-observation client.
- [ ] Live-verify SEC using the owner's identifying user agent.
- [ ] Live-verify FRED using the owner's API key.
- [ ] Record source restrictions for every initial FRED series.
- [ ] Normalize the first SEC financial facts.

Detailed evidence: `psa_platform/PHASE1_PROGRESS.md`.

## Later phases

2. FMP price, statement, calendar, and news prototype.
3. Deterministic technical-analysis and data-quality engine.
4. Unusual Whales options and dark-pool integration.
5. Source-stamped reporting and immutable track record.
6. Security verification.

No later phase begins until the preceding completion criterion in the controlling roadmap
is satisfied or an explicit exception is recorded.
