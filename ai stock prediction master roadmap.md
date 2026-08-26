# AI Stock Prediction Programme — Master Execution Roadmap

**Version 2 — 2026-08-09.** Supersedes v1 in full. v1's discipline sections were sound and are
carried forward; what changed is listed in §31.

**Purpose.** This document is the single execution plan for the next stage of the
stock-prediction project.

**Primary objective.** Produce a genuinely useful, out-of-sample, economically meaningful
prediction system — not another research report.

**Execution rule.** Claude executes this roadmap autonomously, in order, and does not
repeatedly stop to ask what to do next. Stop only for: items marked **HUMAN DECISION
REQUIRED** (§27), destructive actions outside the stated scope, credentials/access problems,
or contradictory frozen evidence that cannot be resolved from the rules below.

---

## 0. Current state — do not restart what is already done

The V2 → V2.3 alpha research line is **CLOSED**, independently audited, and committed. The
authoritative status document is `Stock-Prediction-Models/reports/PROGRAMME_STATUS_V2_3.md`.
Read it before touching anything in the programme.

| | |
|---|---|
| Research status | **CLOSED** — V2 / V2.1 / V2.2 / V2.3 |
| Architecture tested in V2 → V2.3 | **ABANDONED** |
| Production | weight **0**, action **HOLD** |
| Frozen V2.1 exam | **SEALED** — 72 cutoffs, digest `b55e065f4c9f91737b7a56fd715f0913cf8f41207bdb24d91452c10bc1c98ab0` |
| Evidence commit | **`db97386`** on branch `streamlit-app`, 71 files, **not pushed** |
| Independent audit | 2026-08-08 — closure **confirmed by re-derivation**, not accepted from prose |
| Tests at closure | **625 passed**, none skipped (155 of them the research record) |

**V2.3 outcome:** all five gates failed for both eligible arms. V2.3-B vs B3 = **−0.00120**.
The best advantage available anywhere on either λ curve was **+0.00045**, against a measured
resolution of **0.00827** — below the study's ability to see.

### 0.1 Standing prohibitions — carried forward unchanged

From `V2_1_LADDER_PREREGISTRATION.md` §5.2 and `V2_3_PREREGISTRATION.md` §9, restated in
`PROGRAMME_STATUS_V2_3.md` §6. This roadmap may **add** prohibitions; it may not drop one.

* The 72 exam cutoffs are never opened, scored, inspected, modified, deleted or rebuilt.
* Production weight is not raised, and `alpha/adapter.py` is not modified to force a signal.
* No threshold is lowered, no λ re-chosen, no benchmark swapped, no B3 modified.
* No rung, λ point or noise control is promoted to an arm.
* No result is restricted to a regime bucket in order to make it survive.
* Development numbers are never reported as alpha.
* No frozen V2/V2.1/V2.2/V2.3 artefact or preregistration is modified.
* No duplicate evidence-preservation commit is created — `db97386` already exists.
* **No V2.4.** Do not start one by adding another learner to the same information.

### 0.2 What V2.3 established, and what it did not

It did **not** establish that stock prediction is impossible. It established something
narrower:

> Within the tested universe, history, cross-sectional formulation, target/horizon and current
> price/volume-derived feature space, the investigated learning architectures did not
> demonstrate reliable incremental predictive value over the momentum baseline or the B3
> regime rule.

What was not tested is **untouched, not vindicated**. Therefore the next programme must change
the *information and the problem formulation*, not the model complexity.

### 0.3 Nine settled findings — re-testing these spends the same power twice

From `reports/V2_3_POST_MORTEM.md` §5. Treat as answered.

1. Stock-level cross-sectional price/volume features do not rank the cross-section. 18
   absolute features: +0.0084 IC. Adding 47 relative/percentile features: +0.0085. Well-powered
   null over 423 cutoffs.
2. A learned map cannot carry a factor of this strength. `E[target_rank | z__ret_12_1]` spans
   0.023; the leaf-mean SE is 0.029. **The signal is narrower than the instrument.**
3. A factor must be in the output combination, not merely in the input.
4. V2.2-B's +0.00241 was not a diluted signal awaiting authority. Authority ×5.8 → **−0.00052**.
5. A bounded contextual adjustment does not improve on the hand-coded regime rule B3.
6. The whole feature set is worth **+0.0005 to +0.0014 of IC** over one momentum rank.
7. **No tilt pays for its own trading.** Net advantage +0.00028 / +0.00002, intervals spanning
   zero, turnover up 36–56%.
8. The bounded blend does not manufacture IC from rank mechanics (30 noise draws, 0–3%
   exceedance).
9. **Power is the binding constraint, not cleverness.** See §2.6 — this is the most important
   line in the record.

The strongest thing the programme produced is a **three-line hand-specified regime switch with
nothing fitted** (B3, +0.02836) — the only benchmark whose confidence interval excludes zero.
Eleven fitted arms did not beat it.

---

## 0.4 Execution environment — read before running anything

Not optional trivia; each item below has already cost a debugging cycle.

| | |
|---|---|
| Repository | `Desktop/AI Stock/Stock-Prediction-Models`, branch `streamlit-app`. **The parent `Desktop/AI Stock` is not a git repository** — this roadmap and the directives live outside the worktree |
| **`origin` remote** | **`huseinzol05/Stock-Prediction-Models` — a third party's public repository.** Never push. Repoint to a repository the author owns first, or keep the branch local permanently |
| Virtualenvs | `./venv` is a strict superset and runs everything **including pytest**. `./.venv` is what produced the frozen artefacts and matches the recorded run commands but **has no pytest**. Package versions are identical. Use `venv` unless reproducing a recorded command verbatim |
| Console encoding | cp1252. A script printing `−` (U+2212), `✓` or similar dies mid-output with `UnicodeEncodeError`. Use ASCII in stdout |
| Untracked work | `validation/` (a distinct study, see §3.2) and the current app changes are untracked and unpreserved |
| Re-running a ladder | overwrites frozen evidence. Check `V2_3_REPRODUCTION_CHECKLIST.md` "before you start" before invoking any `alpha.ladder_*` module |

**Where the record lives:**

| Path | What |
|---|---|
| `reports/PROGRAMME_STATUS_V2_3.md` | authoritative status |
| `reports/V2_3_EVIDENCE_MANIFEST.md` | what is preserved, what is excluded and why, SHA-256 of 14 artefacts |
| `reports/V2_3_REPRODUCTION_CHECKLIST.md` | 8 tiered checks; **checks 1–6 need nothing but the commit** |
| `reports/V2_3_POST_MORTEM.md` | belief chain, six reasoning errors, what is settled |
| `reports/V2_3_FINAL_DECISION_AUDIT.md` | the independent audit |
| `reports/directives/` | the directives each study was commissioned under |
| `alpha/` | 25 modules, 15 protocol documents, frozen per-cutoff series |
| `validation/REPORT.md` | the separate point-in-time single-name study |

---

## 1. North-star objective

The project succeeds only when it produces a system that can:

1. Generate predictions for unseen future periods.
2. Produce economically meaningful directional signals.
3. Demonstrate predictive value on strictly out-of-sample data.
4. Remain useful **after transaction costs and realistic turnover**.
5. Beat appropriate simple baselines by a pre-defined margin.
6. Remain reasonably stable across time and regimes.
7. Produce **calibrated** confidence/probability estimates.
8. Convert predictions into a portfolio decision without leakage.
9. Survive a final untouched exam.
10. Be integrated into the application only after all evidence gates pass.

The eventual product output, per name:

```
Stock:               NVDA
Direction:           BUY / HOLD / SELL
Expected return:     +X%
P(positive return):  Y%
Confidence:          Z%
Signal:              -100 .. +100
Horizon:             N trading days
Contributing features
Model version
Prediction timestamp
Data cutoff timestamp
```

The exact UI is secondary. Predictive validity comes first.

### 1.1 Two research objects — the instrument and the product

v1 promised per-stock output while prescribing purely cross-sectional metrics (IC, rank IC,
long-short spread, top-N). These are **different studies with different baselines and very
different power**, and conflating them is how the V1 system shipped a signal that lost to
always-predicting-up. The resolution, binding on every phase below:

* **The cross-section is the research instrument.** Information-only tests (Phase 5) and the
  first model (Phase 6) run cross-sectionally, because that is where the tooling, the frozen
  protocol and the statistical power already exist.
* **The single name is the product.** Anything surviving the cross-sectional ladder must pass a
  **separate single-name re-validation (Phase 7b)** against always-up and no-change before it
  may inform the application.
* A signal validated only cross-sectionally **may not be shipped as a per-stock call.**

---

## 2. Global rules for every future study

These bind every stage below.

### 2.1 Point-in-time discipline

Every feature must have been available at the prediction timestamp.

* **A source with no publication timestamp is inadmissible** — not merely risky, not
  "use with care". If you cannot say when a value became knowable, it does not enter the panel.
* Timestamp semantics must be **documented and pinned by a test** before the source is used.
* Fundamentals: use the filing/publication timestamp, not the fiscal-period end. Account for
  reporting lag. Prevent later revisions from entering historical observations.
* News: publication timestamp; never an article published after the cutoff.
* Market data: only bars available at the cutoff; no revised or future aggregates.
* Analyst estimates/revisions: the value **as it existed on that date** (a vintage, not a
  current snapshot).
* Adjusted prices are a known, accepted exception, already documented in
  `validation/README.md`: split and dividend adjustments made after a cutoff are baked into the
  level before it. Splits leave returns untouched; dividend adjustment shifts them by the yield.
  Any new source gets the same explicit treatment — stated, not hidden.

### 2.2 Walk-forward only

No random train/test split for the primary evaluation. Chronological training → validation →
test, with purge and embargo wherever targets overlap. Where cutoff spacing equals the horizon,
windows are non-overlapping by construction — say so, and still bootstrap.

### 2.3 Baselines are mandatory

Every experiment compares against **all** of:

| Baseline | Why it is on the list |
|---|---|
| **B3 regime rule** | **the incumbent.** +0.02836, the only benchmark whose CI excludes zero. Eleven fitted arms failed to beat it. This is the number to beat, not one of four options |
| 12-1 momentum | the factor V2 → V2.3 could not improve on |
| **Always-predict-up / unconditional drift** | **the baseline that actually beat the last per-stock system.** `validation/REPORT.md`: 0 of 9 components beat it, unanimous sign. Mandatory for anything single-name |
| **No-change / "price won't move"** | beat the consensus price targets 62% of the time and the LSTM path 77%. Mandatory for any level or price-target output |
| Buy-and-hold / market | where appropriate |
| A simple non-learning factor model | chosen by economic prior, **not** by whichever has the best in-sample \|IC\| |
| The simplest possible version of the new information source | one rank, one ratio, one z-score |

**If the new information cannot beat the relevant simple baseline, stop that branch.**

### 2.4 No metric shopping

Before inspecting any test result, fix in writing: primary metric, secondary metrics, success
threshold, failure threshold, minimum sample size, stability requirements, economic threshold.
Do not then select whichever metric happens to look good.

### 2.5 No regime cherry-picking — and a regime-concentrated result is a disqualifier

Do not rescue a failed model by reporting only one regime, sector, year, λ, stock subset or
horizon. Regime analysis is a **pre-defined diagnostic only**.

**Strengthened from v1.** `BEAR_TREND` was the only bucket in which any arm improved on its
base — in V2, V2.1, V2.2 *and* V2.3. It is 27 cutoffs, 17 of them (63%) in 2022, and V2's edge
there **inverted out of sample**. This was recorded as a caveat four times before V2.3 made it
a formal abandonment criterion. It should have been one two studies earlier.

> A result that lives entirely inside 17 weeks of one bear market is a single observation, not
> a factor. Concentration in one regime bucket **disqualifies**; it does not caveat.

### 2.6 Power before permission — the blocking pre-study gate

**This is the rule whose absence cost four studies.** No study may be run before this gate is
passed, and passing it is arithmetic, not judgement.

1. **State the smallest effect worth acting on**, derived from the economic threshold and the
   cost model — not from what the model might plausibly produce.
2. **Compute the half-width the planned design will achieve** — cutoff count, spacing,
   universe, and pairing against the base — using the same moving-block bootstrap the record
   uses (`alpha/stats.py`, `BLOCK_LENGTH = 4` cutoffs; `block_bootstrap_ci`,
   `block_bootstrap_p`, `newey_west` and `paired_difference` already exist and should be
   reused, not rewritten).
3. **If the achievable half-width exceeds the effect sought, the study may not run as
   designed.** Change the horizon, the cutoff count, the history depth, the universe, or the
   size of effect being chased — or do not run it. Running it anyway produces an unfalsifiable
   null and burns a family from the §21 budget for nothing.

**Calibration from the record, so no one re-derives it:**

| Measurement | Value |
|---|---|
| Measured half-width, V2.3-A vs B1, 255 paired cutoffs | **0.00827 IC** |
| Same, scaled to 72 cutoffs | 0.01556 |
| V2.3-B vs B3, 255 cutoffs | 0.00796 |
| ~10 years at weekly non-overlapping spacing | ~500 cutoffs maximum |
| **Floor of what this history can resolve against a correlated base** | **~0.006 IC** |
| Cutoffs needed to resolve V2.1-D's edge over momentum | ~1,750 (~35 years) |
| Cutoffs needed to resolve V2.3-B's −0.00120 against B3 | **~11,000 (~220 years)** |

Two consequences that must be stated in every V3 preregistration:

* **The entire 34-column V2 feature set is worth +0.0005 to +0.0014 IC. V3 must therefore be
  hunting an effect 5–10× larger than anything V2 ever found, or it is unrunnable on this
  history.** "Somewhat better than V2" is not a fundable hypothesis.
* **Effective *n* is the cutoff count, not the row count.** Four hundred names on one date are
  not four hundred observations. `validation/README.md` already records this as the binding
  constraint: "twelve cutoffs is twelve effectively independent market draws, and no amount of
  extra symbols relaxes it." All intervals cluster by date.

This reframes the Phase 2 ranking criterion: rank candidates by **expected effect size relative
to the study's resolution**, not by "expected signal" in the abstract.

### 2.7 Multiple-testing control and the experiment registry

Every experiment records: hypothesis, features, target, horizon, model, hyperparameters, seeds,
evaluation period, baseline, result. **The number of arms and hypotheses is declared before the
first fit**, and the significance criterion accounts for them. Maintain the registry (§3.3).
Never silently discard a failed run.

### 2.8 Frozen evidence

Once a study is final: freeze its artefacts, hash them, record the exact configuration and code
version, never overwrite silently. `reports/V2_3_EVIDENCE_MANIFEST.md` is the working template.

### 2.9 No architecture escalation before information evidence

Do not walk tree → deep learning → RL → transformer because a model failed. First determine
whether the **information** contains incremental predictive signal (Phase 5). A family that
fails its information-only test is **not** re-tested with a larger model.

### 2.10 Admissibility — what counts as genuinely new information

v1 forbade architecture escalation but left the door open to a V2.4 with fresh paint. Closing
it: a candidate information dimension is admissible only if **all** hold.

1. **It is not computable from `alpha/cache`.** A transform of price and volume is inside the
   space V2.3 already refuted, however clever the transform.
2. **It carries its own timestamp** (§2.1).
3. **It clears a correlation ceiling** against `z__ret_12_1` and against the existing 34-column
   feature set, measured on the panel before any model is fitted.
4. **Its plausible effect exceeds the study's resolution** (§2.6).

Adding two columns to V2's inputs is a V2.4 and is prohibited by §0.1.

### 2.11 Sanity controls need the same power discipline as gates

V2.3's §4 noise control specified **one** seeded draw compared on **unpaired** means, with the
instruction that any gain ends the study. The seed landed ~2σ high and produced a +0.00123
"gain" on pure noise, and the first ladder run aborted on it. Over 30 paired draws the blend
destroys IC (−0.00202 / −0.00278; 3% / 0% of draws above base) — the single-draw spread
(0.00137) was comparable to the effect it was meant to detect.

> Pair the control, and use enough draws that its sampling spread is small against the effect.
> A control that can fire on noise is not a control.

### 2.12 A free power gain is a warning, not a gift

`V2_3_RESEARCH_DESIGN.md` §6 reported bounded arms as **~19× better powered** and banked it as
a methodological improvement. It was collinearity: an arm 99.2% correlated with its base has
almost no paired variance against that base, which is the same statement as "it barely differs
from it". Real authority rose 5.8× and the interval widened 4.5× — near-proportional.

> **Resolution and authority are the same dial.** An arm can be precisely measured, or it can
> be free to differ from its base. It cannot be both. A power advantage that appears for free
> should be read as evidence the arm is doing nothing.

### 2.13 Never reason from a post-processed number about a fitted model

The **+0.00604 "orthogonal component"** that funded V2.3 was produced by projecting an existing
model's predictions off the base. It did not survive being learned: a model trained to predict
a residual *without seeing the base* produces a different and worse adjustment. The design pass
correctly refused to make post-processing an arm — and then kept reasoning from its number
anyway. If a quantity is worth acting on, fit it; if it is not worth fitting, it is not
evidence.

---

## 3. Phase 1 — confirm the base, decide `validation/`, open the registry

**Objective:** a clean starting point. Most of v1's Phase 1 is already done, audited and
committed; only three deltas remain.

### 3.1 Confirm nothing drifted (do not re-audit)

The full verification was executed and independently re-derived on 2026-08-08 at `db97386`.
Do **not** re-run the audit. Run `reports/V2_3_REPRODUCTION_CHECKLIST.md` **checks 1–6** —
they need nothing but the commit — and confirm:

| Check | Expected |
|---|---|
| 1 — exam seal recomputes | `b55e065f…`, 72 cutoffs |
| 2 — exam refuses to open | `alpha.v2_1_exam predict` exits 1 on the closed §5.2 gate |
| 3 — production weight | `0.0`, all seven criteria False |
| 4 — V2.3-B vs B3 re-derived | −0.00120, breadth 0.451, halves −0.00034 / −0.00206 |
| 5 — exam contamination | 0 across ten frozen series |
| 6 — test suite | 625 passed, none skipped (use `./venv`) |

Any mismatch is a §27C fundamental contradiction — stop and report it.

### 3.2 Decide `validation/` — preservation, not a fresh audit

`validation/` is a **separate point-in-time study** and remains untracked and unpreserved. Its
research question, design, leakage controls and results are already written up in
`validation/REPORT.md`, and its conclusions are recorded — do not re-derive them:

* No component beat always-predicting-up on its own horizon — **0 of 9, unanimous sign.**
  Consensus 53.7% directional (p = 0.54); best agent 56.9%; LSTM 59.4% but 72% bullish against
  a 64.6% up-rate.
* **The neural forecast changed zero verdicts** — the significance gate fired 257 of 257
  horizon-slots. Adding it is provably a no-op, not a weak effect.
* The 4-hour horizon is inverted when read after the close (20.8% on acted calls, p = 0.009),
  scoped to after-close reads because every scored window straddles an overnight gap.
* Price targets and the LSTM path lose to "price won't move".
* **Vindicated:** the HOLD floor and the significance gates. It abstained on 74.3% of
  symbol-dates, and on the calls it made its edge over a trivial rule was zero. **Do not loosen
  `MIN_T`, `MIN_CONFIDENCE` or `FAMILY_CAP` (`app/core/ultimate.py`) on the strength of a fit.**

What is actually open, and what Phase 1 must settle:

1. **Preservation.** It is a real study with a real result and it is not under version control.
   Preserve it the way V2.3 was preserved — its own evidence commit, manifest entry and hashes.
2. **Harness reuse.** `validation/pit.py`'s one-door fetcher, the two-process
   predict/score split, and `test_future_cannot_change_the_verdict` are exactly the machinery
   Phase 7b needs. Decide what is reused as-is versus rebuilt.
3. **Do NOT merge its results into V2/V2.3.** Different study, different question, separate
   record.

### 3.3 Open the permanent experiment registry

Create **`reports/EXPERIMENT_REGISTRY.md`** — in `reports/`, not a new `research/` tree (§25).

Fields per experiment: ID · date · hypothesis · information source · target · horizon ·
universe · features · model · hyperparameters · training period · validation period · test
period · baseline · **pre-registered resolution and MDE (§2.6)** · primary metric · result ·
decision (CONTINUE / REJECT / INCONCLUSIVE) · reason · commit/hash.

**Seed it with the eleven V2 → V2.3 arms** from the frozen record so it begins as a true
history rather than an empty form.

### Exit condition

No new modelling begins until checks 1–6 pass, the `validation/` decision is recorded, and the
registry exists and is seeded.

---

## 4. Phase 2 — Information audit under the free-data constraint

**Objective:** find information dimensions V2.3 did not test, that are *obtainable*, *properly
timestamped*, and *plausibly large enough to see* (§2.6).

### 4.0 The binding constraint — HUMAN DECISION already taken

**Free sources only. No data-provider spend is authorized** (§27B). This is not a preference to
be re-opened by an autonomous run mid-study; it is a fixed constraint on the audit.

v1 ranked fundamentals, earnings surprise, analyst revisions and news highest. Under the free
constraint, the audit must be honest about which of those are reachable at all.

### 4.1 Struck — not obtainable free with usable point-in-time semantics

| Struck | Why |
|---|---|
| Consensus estimates, and therefore **earnings surprise vs consensus** | no free historical consensus with as-of dates |
| **Analyst estimate revisions** | same |
| **News / sentiment archives** (family E, largely) | no free historical archive with reliable publication timestamps at scale |
| yfinance fundamentals | restated, no filing dates — **inadmissible under §2.1**, not merely weak |

These are struck for *availability*, not because they lack signal. Record them in the audit as
blocked-on-data so the reason survives.

### 4.2 The free, genuinely timestamped shortlist — verify these first

The honest answer under the free constraint is better than v1 assumed: a real
publication-timestamped information space exists at zero cost. **Each row is a candidate whose
timestamp semantics the audit must verify and pin with a test (§2.1) before use — not an
established fact.**

| Source | What it carries | Point-in-time basis to verify | Coverage to check |
|---|---|---|---|
| **SEC EDGAR XBRL `companyfacts`** | reported fundamentals per filing — revenue, EPS, margins, cash flow, debt, book value | each fact carries its filing date and accession, so restatements are *visible* rather than silently overwriting history | US filers; XBRL mandate era onward |
| **SEC Form 4** | insider transactions | transaction date *and* filing date both present | all §16 filers |
| **SEC 13F** | institutional holdings, quarterly | filing date; ~45-day statutory lag must be respected, not assumed away | managers over the reporting threshold |
| **FRED / ALFRED** | rates, yield curve, credit spreads, USD | **ALFRED serves vintages** — the value as it stood on a past date, which is the whole point | macro series, long history |

Note what this makes reachable that v1 assumed was not: **realized** earnings growth,
acceleration, margin change and post-earnings drift measured from the *filing timestamp* are
free and PIT-clean via EDGAR. Only the *consensus-relative* versions are blocked.

### 4.3 Families C and D fail admissibility as standalone candidates

Market structure (volatility regime, realized volatility, relative strength, trend persistence,
volume anomaly, liquidity, breadth, dispersion, correlation regime) and cross-asset context
computed from ETFs are, with few exceptions, **derivable from `alpha/cache`** and therefore
fail §2.10 clause 1 — they are inside the refuted space.

They remain legitimate as **context/conditioning variables** alongside an admissible family
(the B3 regime switch is exactly this, and it is the incumbent). They are not admissible as the
*new information* that justifies a V3.

### 4.4 Scoring — three criteria are vetoes, not scores

Score each candidate on: expected effect size, PIT quality, availability, implementation cost,
leakage risk, priority. But three act as **vetoes**:

* **No publication timestamp → out** (§2.1).
* **Derivable from the existing cache → out** (§2.10).
* **Plausible effect below the study's resolution → out** (§2.6).

### 4.5 Deliverable

`reports/INFORMATION_AUDIT.md`, with the scoring table, the struck list with reasons, and the
verified timestamp semantics of each surviving source.

**Output: at most three families, named and frozen before the first study** (§21). Do not
implement everything at once.

---

## 5. Phase 3 — Redefine the prediction target

**Objective:** stop optimizing for microscopic IC improvements; evaluate whether the system
should predict an economically meaningful event. Test a small, pre-defined set.

| Target | Definition |
|---|---|
| **A — forward return** | 5D / 10D / 20D. Only horizons justified by data and trading practicality |
| **B — directional return** | positive vs negative forward return |
| **C — economically meaningful move** | e.g. BUY ≥ +5%, HOLD between −5% and +5%, SELL ≤ −5%. Thresholds fixed **before** final testing and justified against volatility, costs and sample size |
| **D — risk-adjusted direction** | forward return exceeds a volatility-adjusted threshold |

**Mandatory comparison.** For each target determine: adequate sample size; stable class
balance; economic meaning; predictable without leakage; compatible with portfolio construction;
**and its power implication under §2.6** — a target with a larger effect and fewer usable
cutoffs may be strictly better than a target with a tiny effect and many. State the achievable
half-width per target alongside its sample size.

Do not assume classification beats regression. Note that Target C's coarser classes are
plausibly a *larger* effect than a rank IC, which is precisely what §2.6 says to look for.

**Deliverable:** `reports/TARGET_DESIGN.md`.

---

## 6. Phase 4 — Build the new information pipeline

**Objective:** implement only the highest-priority dimensions from Phase 2.

For each feature define: exact mathematical construction · timestamp semantics · missing-value
handling · survivorship handling · winsorization/normalization · cross-sectional vs time-series
calculation. Then write leakage tests, unit tests, and verify availability at every historical
cutoff.

### 6.1 Reuse the one-door design — do not invent a new one

`alpha/pitdata.py` already solves this problem and its guarantee is tested. Mirror it:

* Truncation happens in **exactly one place** (`PriceBook.view(cutoff)` → `PriceView`).
* A view has **no method that can reach past its own edge**; full history is reachable only
  from the book.
* The only forward-reading method is named to be greppable (`forward_return`) and is called
  exclusively from the scoring side.
* The guarantee is proved by a test that **rewrites the future and demands an identical
  verdict** — `test_future_cannot_change_the_verdict`. Any leak anywhere turns it red.

A filings panel needs the same shape with one addition: because EDGAR facts carry both a
*period* and a *filing date*, the door must filter on **filing date ≤ cutoff**, and a test must
prove that a later restatement of an earlier period cannot enter a historical observation.

### 6.2 Required test categories

Future-timestamp rejection · publication lag · missing data · delisted assets · duplicated
records · **restatements and revisions** · universe membership · NaN propagation · train/test
contamination.

**Deliverable:** a point-in-time feature dataset with metadata.
**Do not proceed if timestamp semantics are uncertain** — under §2.1 that source is
inadmissible, not provisional.

---

## 7. Phase 5 — Information-only tests

The most important phase. Before any sophisticated ML: **does this information contain
predictive signal at all?**

**Precondition:** the §2.6 power gate is passed and recorded in the preregistration. A family
tested below its resolution yields an unfalsifiable null and still consumes one of the three
budgeted slots — which is the worst possible outcome.

For each admissible dimension:

| Test | |
|---|---|
| 1 | Simple rank/quantile portfolio |
| 2 | Univariate regression |
| 3 | Long-short spread |
| 4 | Information coefficient |
| 5 | Temporal stability (chronological halves, yearly) |
| 6 | Sector and regime stability — **concentration disqualifies (§2.5)** |
| 7 | Incremental value over 12-1 momentum **and over B3** |

If a family fails every simple test, **do not feed it into a complex model** (§2.9).

**Decision categories:** **A** — evidence of useful information → continue. **B** —
weak/inconclusive → do not optimize heavily; gather more evidence, or combine only if
justified. **C** — no evidence → reject the family and spend a budget slot (§21).

---

## 8. Phase 6 — Build the first V3 model

Only after Phase 5 identifies useful information.

**Model hierarchy — start simple:** linear/logistic → regularized regression → gradient-boosted
trees → random forest / extra trees where justified → the existing learner only if appropriate.

**Do NOT begin with** reinforcement learning, DQN, policy gradient, recurrent RL, or
transformers. Complexity must earn its place (§2.9, §23, §24).

```
Price/Volume Information
        +
New Information Dimension(s)          <- must satisfy §2.10
        +
Market/Regime Context                 <- conditioning only, not the new information
        v
   Feature Layer
        v
 Simple Predictive Model
        v
 Probability / Expected Return
        v
 Calibration
        v
 BUY / HOLD / SELL
```

---

## 9. Phase 7 — V3 walk-forward validation (cross-sectional)

Run chronological walk-forward. Record per cutoff: prediction, realized outcome, probability,
expected return, benchmark outcome, model version.

**Predictive metrics:** IC · rank IC · directional accuracy · balanced accuracy · precision ·
recall · F1 where useful · ROC-AUC where appropriate · PR-AUC for imbalanced events · Brier
score · calibration error.

**Economic metrics:** average forward return · long-short spread · cumulative return · Sharpe ·
Sortino · max drawdown · turnover · **transaction-cost-adjusted return (the primary one, §10)**.

**Stability:** chronological halves · yearly · market regimes · sectors · volatility regimes.

**Intervals:** cluster by cutoff date and use the moving-block bootstrap in `alpha/stats.py`
(block length 4 cutoffs) as the headline interval, with Newey-West as a cross-check. Report the
achieved half-width next to every point estimate — a point estimate without its resolution is
not a result (§2.6).

## 9b. Phase 7b — Single-name re-validation (new, and blocking)

Nothing reaches the application on cross-sectional evidence alone (§1.1). Anything surviving
Phase 7 is re-scored **per symbol, on its own terms**:

* Predictions frozen before outcomes are revealed, in two processes, as `validation/predict.py`
  and `validation/score.py` already do — the code that sees outcomes cannot reach the code that
  makes predictions.
* Scored against **always-predict-up** and **no-change** (§2.3), on the actual up-rate of the
  period rather than against 50%.
* Abstention is counted, not hidden: report the share of symbol-dates on which the system
  declines to call, and measure the edge **on the calls it makes**.
* Intervals clustered by cutoff date — thirty symbols on one day are not thirty observations.

A signal that beats the cross-section but not always-up is a portfolio-construction result, not
a stock prediction, and must be described as one.

---

## 10. Phase 8 — The "Working Model" gate

A model is **not** successful because accuracy > 50%, one year looks good, one stock looks
good, one regime works, a backtest is profitable, or a complex model beat one weak baseline.

A candidate becomes a **Working Model** only if it satisfies **all** pre-registered gates:

1. Positive out-of-sample primary metric.
2. Confidence interval excludes the null where statistically appropriate.
3. Beats 12-1 momentum by a meaningful, pre-declared margin.
4. **Beats B3** — the incumbent, and the only benchmark whose CI excludes zero.
5. **Economic return survives realistic transaction costs — net, not gross.** V2.3 settled that
   no tilt pays for its own trading (net advantage +0.00028 / +0.00002, intervals spanning zero,
   turnover up 36–56%). **Net-of-cost is the primary economic metric from the first
   measurement, not a later sanity check.**
6. Performance is not concentrated in one tiny period or one regime bucket (§2.5).
7. No material leakage found.
8. Calibration is acceptable (§12).
9. Turnover is economically reasonable.
10. **Passes Phase 7b single-name re-validation** if it is to reach the application.
11. Performance survives a final untouched evaluation (§15).

**Exact numerical thresholds, the arm count, and the achievable resolution are fixed in the
preregistration BEFORE the final evaluation.** No rung, λ point or noise control may be
promoted to an arm afterwards (§0.1).

---

## 11. Phase 9 — Model combination / ensemble

Only if multiple **independently validated** models contain useful information.

```
Momentum Model + Fundamental Model + Market-Regime Model + Event Model
                              v
                          Meta Model
                              v
                 Probability / Expected Return
                              v
                       Calibrated Signal
```

Rules: each component needs independent evidence; no ensemble may hide a failed component;
meta-model training must be strictly out-of-sample with respect to component predictions; avoid
stacking leakage. Compare individual models, simple average, weighted average, and a simple
meta-model. **Prefer the simplest ensemble that works.**

---

## 12. Phase 10 — Confidence / probability calibration

The application needs a confidence value that means something. If the model says 80%, then
historical predictions near 80% should be positive roughly 80% of the time.

Test: reliability curves · Brier score · calibration slope and intercept · expected calibration
error · probability bins. **Do not label raw model scores "confidence".**

---

## 13. Phase 11 — Signal engine

Once a validated model exists, define **Direction** (BUY/HOLD/SELL), **Signal** (model output
mapped to −100…+100), **Confidence** (calibrated probability, §12), **Expected return** (for
the chosen horizon), and **Risk** (expected volatility, downside probability, drawdown risk
where feasible).

The signal engine must be deterministic and testable.

---

## 14. Phase 12 — Portfolio simulation

Only after prediction validity is demonstrated. Test top-N · threshold-based · long-only ·
long/short only if appropriate · position caps · sector caps · volatility scaling · turnover
limits. Include spread, commissions, slippage, liquidity constraints and rebalance frequency.
Compare against market, momentum, B3 and a simple factor portfolio.

---

## 15. Phase 13 — Final untouched exam

The V2.1/V2.3 discipline, applied to the V3 architecture. This discipline held under four
consecutive disappointments and is the most valuable asset the programme owns.

**Before running it, freeze:** protocol · target · features · model · hyperparameters ·
thresholds · benchmark · portfolio rules · success criteria. Then **hash the exam set**.

Then: **DO NOT TOUCH THE EXAM. Run once.**

**The exam must be adequately powered before it is sealed** (§2.6) — V2.1's own directive
required ≥60 non-overlapping cutoffs for exactly this reason, and a 12-date exam could not
support its criterion 7 at all. Sealing an underpowered exam wastes the one shot.

Outcomes — **SUCCESS**, **FAILURE**, **INCONCLUSIVE** — are all valid scientific results.
Failure is pre-registered as a first-class outcome.

---

## 16. Phase 14 — Paper trading / live shadow mode

Only after exam success. Run predictions without capital first. Record every prediction
**before** the outcome: timestamp · asset · signal · probability · expected return · model
version · feature-snapshot hash. Then compare to reality.

Define the minimum shadow period before beginning. **Do not modify the model continuously
based on live outcomes without opening a new research version.**

---

## 17. Phase 15 — Production integration

Only after shadow validation. Requirements: versioned model · versioned feature pipeline ·
reproducible prediction · data-freshness monitoring · missing-data handling · model-health
monitoring · prediction logging · calibration monitoring · drift detection · fail-safe
behaviour.

If a valid prediction cannot be produced: **return HOLD / unavailable. Never fabricate a
signal. Production fails closed.**

---

## 18. Phase 16 — Application integration

Only after the predictive engine is independently validated, **including Phase 7b**.

* **Forecast tab** — expected return, probability, confidence, horizon, prediction date.
* **Positions table** — call, signal −100…+100, confidence %.
* **Charts** — historical predictions, actual outcomes, prediction accuracy, calibration,
  regime performance.
* **Audit panel** — model version, data cutoff, last training date, last validation date,
  signal timestamp.

**The UI must not imply certainty.** And the existing abstention machinery stays: the HOLD
floor and significance gates are the one part of the V1 engine that measurement vindicated
(§3.2). Do not loosen `MIN_T`, `MIN_CONFIDENCE` or `FAMILY_CAP` to make the UI look more
decisive.

---

## 19. Phase 17 — Continuous monitoring

**Data:** missing features · delayed feeds · distribution shifts · universe changes.
**Model:** feature drift · calibration · directional accuracy · IC · economic return · turnover
· drawdown.
**Performance:** rolling 20/60/120 prediction windows · regime performance · benchmark
comparison.

Automatic HOLD conditions:

```
IF   data invalid
OR   calibration breaks
OR   model drift exceeds threshold
OR   production integrity check fails
THEN production weight = 0
     signal = HOLD
```

---

## 20. Phase 18 — Retraining policy

Never let automatic retraining become uncontrolled research. Define in advance: retraining
frequency · training window · feature version · model version · validation gate · rollback
rule. Every new model passes the same validation process. **No silent replacement.**

---

## 21. Budget and termination — pre-registered, not a judgement call

v1 said "decide whether another information dimension is justified", which is an open loop —
and the open loop is exactly what the post-mortem identifies as the programme's central failure
mode: four studies asking one question four ways, each null followed by a new excuse.

**Pre-registered budget: three genuinely independent information families (§2.10). No fourth.**

* A family that fails its Phase 5 information-only test is **REJECTED and spends a slot**.
* A rejected family is **not re-tested with a larger model** (§2.9), a different learner, or
  "one more carrier". That move is what V2 → V2.3 was.
* **If all three families fail, the programme concludes that the problem formulation — not the
  information — is wrong, and stops.** It does not open a fourth family. Reconsidering the
  formulation is a new programme with a new directive, commissioned deliberately, not a
  continuation.

Before rejecting a family, diagnose honestly and record it in the registry: did the
*information* fail, or the target/horizon, the point-in-time quality, the sample size, the
economic significance, or the **power** (§2.6)? A family killed by insufficient resolution was
never tested and should be recorded as such — but it still spends its slot, which is the point
of the §2.6 gate.

This budget is fixed in the same spirit as `V2_3_PREREGISTRATION.md` §9: its entire value is
that it was written before there was a result to protect.

---

## 22. If V3 succeeds

Do not deploy. Each stage passes independently:

```
Information signal -> Simple model success -> Walk-forward success ->
Single-name re-validation (7b) -> Calibration -> Economic backtest (net of costs) ->
Final untouched exam -> Shadow/paper trading -> Production
```

---

## 23. When to consider deep learning

Only after evidence shows: the information contains useful signal · simple models can exploit
it · there is enough data to justify higher capacity · the simple model has reached a
**measurable** ceiling · the deep model has a clearly defined expected advantage.

Then test MLP → temporal model → transformer/time-series architecture, under the same
walk-forward and exam discipline. Note §2.6 applies unchanged: higher capacity does not buy
resolution.

---

## 24. When to consider reinforcement learning

RL must **not** be used to discover whether a predictive signal exists. Consider it only after
a predictive signal exists, the prediction engine is validated, portfolio construction itself
has become the research problem, and the action/reward formulation is justified.

RL would then answer *"how should the portfolio allocate given validated forecasts?"* — not
*"can RL magically predict stocks?"*

---

## 25. Required documents — mapped onto the existing record

v1 prescribed a `research/` tree. **Do not create one** — it would fragment a record that
already has a working convention. Use what exists:

```
alpha/                              # study code and per-study protocol documents
├── V3_RESEARCH_DESIGN.md
├── V3_PREREGISTRATION.md
├── V3_EXPERIMENT_LOG.md
└── V3_LADDER_REPORT.md

reports/                            # programme-level record
├── EXPERIMENT_REGISTRY.md          # NEW - §3.3, seeded with V2-V2.3
├── INFORMATION_AUDIT.md            # NEW - §4.5
├── TARGET_DESIGN.md                # NEW - §5
├── PROGRAMME_STATUS_V3.md
├── V3_EVIDENCE_MANIFEST.md
├── V3_REPRODUCTION_CHECKLIST.md
├── V3_POST_MORTEM.md
└── directives/                     # commissioning directives, incl. this roadmap
```

Do not create documents for appearance. Each must preserve a meaningful decision or a
reproducibility property.

---

## 26. Claude execution protocol

**Before every major experiment:** read the current programme status · read the experiment
registry · read the relevant preregistration · inspect git status · verify no frozen artefact
is about to be overwritten · verify the exam is untouched · **verify the §2.6 power gate is
passed and recorded** · create/confirm the experiment ID · state the hypothesis in the log ·
run it.

**After every experiment:** save raw per-cutoff results · save summary · save configuration ·
record metrics **with their achieved half-widths** · compare to baselines · check leakage ·
check temporal and regime stability · update the registry · decide **CONTINUE / REJECT /
INCONCLUSIVE** · commit only intentional research changes.

**Never:**

* silently change the target, benchmark or thresholds after seeing results;
* inspect the sealed exam;
* overwrite frozen evidence;
* claim success from a single favourable slice;
* increase model complexity because a simpler model failed;
* promote a rung, λ point or control to an arm;
* modify production to create a signal;
* run a study whose resolution cannot see the effect it seeks (§2.6);
* ask the user what to do after every small experiment.

---

## 27. HUMAN DECISION REQUIRED — only these cases

Continue autonomously unless one of these occurs.

**A. Irreversible external action** — publishing research, deploying to production, or
**any `git push`**. Note specifically: **`origin` is `huseinzol05/Stock-Prediction-Models`, a
third party's public repository** (§0.4). A push is not merely irreversible, it would publish
this work into someone else's repo. Repointing the remote is itself a human decision.

**B. Data spend — currently barred.** The free-only constraint (§4.0) is a decision already
taken. If a study appears to require a paid provider, **stop and report it as a §27B item**; do
not purchase, do not trial, and do not silently substitute a lower-quality free source without
recording the substitution in the audit.

**C. Sensitive/private data** — if a source requires personal credentials or private financial
data, stop.

**D. Fundamental contradiction** — if the research record contains contradictory frozen
evidence that cannot be resolved mechanically (including a Phase 1 check-1–6 mismatch), stop
and report.

**E. Final production authorization** — even after successful research, allocating capital
requires explicit human authorization.

**F. Ending the programme under §21** — if all three families fail, report the conclusion and
stop. Do not commission the successor programme autonomously.

Everything else is handled autonomously.

---

## 28. Success definition

The project is **not** complete because a model was trained, a backtest made money, accuracy
exceeded 50%, a neural network beat a tree, an RL agent produced trades, or the UI looks
convincing.

It is complete only when:

```
NEW INFORMATION (admissible, §2.10)
      v
POINT-IN-TIME VALID
      v
EFFECT LARGE ENOUGH TO RESOLVE (§2.6)
      v
OUT-OF-SAMPLE PREDICTIVE SIGNAL
      v
STATISTICALLY CREDIBLE
      v
ECONOMICALLY MEANINGFUL NET OF COSTS
      v
BEATS B3 AND ALWAYS-UP
      v
STABLE ACROSS TIME AND REGIMES
      v
CALIBRATED
      v
SURVIVES UNTOUCHED EXAM
      v
SURVIVES SINGLE-NAME RE-VALIDATION (7b)
      v
SURVIVES SHADOW/PAPER TEST
      v
PRODUCTION
```

---

## 29. Immediate next action

Do **not** start V2.4. Do **not** start another learner comparison. Do **not** touch the sealed
exam.

1. **Phase 1** — run reproduction checklist checks 1–6 (§3.1); record the `validation/`
   preservation decision (§3.2); create and seed `reports/EXPERIMENT_REGISTRY.md` (§3.3).
2. **Phase 2** — the information audit under the free-only constraint, starting from the EDGAR
   / Form 4 / 13F / ALFRED shortlist (§4.2), with timestamp semantics verified and pinned by
   tests. Output at most three families.
3. **Phase 3** — target design, each candidate carrying its power implication (§5).
4. **§2.6 power gate** — for the top family and chosen target, compute the achievable half-width
   and compare it to the smallest effect worth acting on. **If the design cannot see the
   effect, redesign or stop before implementing anything.**
5. **Phase 4 → Phase 5** — implement only the highest-priority dimension and run the first V3
   information-only experiment.

The first objective is not to build the final model. It is to answer:

> **Is there genuinely new, point-in-time information that contains predictable future stock
> information beyond the momentum and regime baselines — and is its effect large enough for
> this history to see?**

If **yes** → build the smallest model that exploits it.
If **no** → reject the family, spend a budget slot (§21), and move to the next genuinely
different source.

---

## 30. Final principle

The programme must stop searching for a clever algorithm and start searching for information
that survives contact with the future — **and it must stop asking questions its data cannot
answer.**

V2.3 did the difficult job of demonstrating that repeatedly increasing architectural complexity
within the same information space is not the path. Its post-mortem did the harder job of
showing why: the effects being chased were smaller than the instrument measuring them.
Resolving V2.3-B's edge would take 220 years of weekly cutoffs. **The effects were absent, not
under-measured.**

The next breakthrough, if there is one, comes from

> better information + better target + strict point-in-time validation + an effect large
> enough to resolve

and not from another complicated learner.

The goal is not another impressive research report. It is a prediction engine that earns the
right to say:

> **"This signal has worked on data the model had never seen before."**

---

## 31. What changed from v1

| Area | Change |
|---|---|
| **§2.6 Power before permission** | **New, and the central addition.** A blocking pre-study gate with the record's measured calibration. v1 had no way to refuse a study it could not resolve |
| §0.4 Execution environment | New. Repo location, the third-party `origin` trap, the two venvs, cp1252 |
| §0.1, §0.3 | Standing prohibitions and the nine settled findings pulled in by citation instead of paraphrase |
| §1.1 Two research objects | New. Cross-section = instrument, single name = product; resolves v1's contradiction between its output spec and its metrics |
| §2.1 | A source without a publication timestamp is now **inadmissible**, not "risky" |
| §2.3 | Added always-up and no-change baselines; named B3 as *the* incumbent |
| §2.5 | Regime concentration is now a **disqualifier**, not a caveat |
| §2.10–2.13 | New rules carrying the post-mortem's transferable lessons: admissibility of "new" information; controls need gate-level power; a free power gain is a warning; never reason from post-processed numbers |
| §3 Phase 1 | Cut from a full re-audit to the three deltas that actually remain |
| §4 Phase 2 | Rewritten under the free-only constraint: what is struck, and the EDGAR/Form 4/13F/ALFRED shortlist that survives. Three veto criteria |
| §9b Phase 7b | New blocking phase — single-name re-validation before anything reaches the app |
| §10 | Net-of-cost is now the primary economic metric from the first measurement |
| §21 | Rewritten from an open loop into a pre-registered three-family budget with a stated termination condition |
| §25 | `research/` tree replaced by the existing `alpha/` + `reports/` convention |
| §27 | Added the `origin` trap by name, the standing bar on data spend, and the §21 termination as a reporting stop |
| Format | Converted from plain text to Markdown; section numbers preserved so existing citations resolve |
