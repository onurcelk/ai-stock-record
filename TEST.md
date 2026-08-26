# Historical Forecast Validation / Point-in-Time Backtest

Perform a rigorous historical validation of the forecasting system.

The objective is to determine how accurately the system would have predicted the future if it had actually been running at a specific point in the past.

## Core Principle: No Look-Ahead Bias

You MUST simulate the system as if the current date were the historical evaluation date.

For every historical test:

* Only use data that was actually available on or before the historical cutoff date.
* Do NOT use any future price data when generating the forecast.
* Do NOT use future technical indicators.
* Do NOT use future news, sentiment, fundamentals, analyst revisions, or events.
* Do NOT allow any Forecast or Agent component to access information from after the cutoff date.
* Do NOT use today's market information when generating the historical prediction.
* Any feature, indicator, model input, or derived value must be calculated using information available at that historical point in time.

The future data may ONLY be revealed after the prediction has been completed, for the purpose of measuring prediction accuracy.

---

# Test Procedure

Run multiple historical forecasting experiments rather than testing only one date.

At minimum, test:

1. Approximately 6 months ago
2. Approximately 3 months ago
3. Approximately 1 month ago
4. Approximately 2 weeks ago

If sufficient historical data is available, also test additional randomly selected historical dates.

For each test date, perform the following sequence.

### Step 1 — Freeze the Information Set

Set the system's effective date to the historical cutoff date.

Example:

If the test date is February 7, 2026, the system must behave exactly as if today were February 7, 2026.

The system must only see data available up to February 7, 2026.

Record exactly what information was available to the system at this point.

---

### Step 2 — Generate the Forecast

Run the normal Forecast system using only the historical information set.

Generate the complete forecast exactly as the production system would have generated it.

Record:

* Directional prediction
* Predicted price
* Expected return
* Forecast horizon
* Confidence
* Signal strength
* Bullish / bearish classification
* Any probability estimates
* Any technical or fundamental reasoning
* Any other forecast outputs

Do NOT modify the forecast after seeing the actual future outcome.

---

### Step 3 — Run the Agent

Run the Agent using the same historical information set.

The Agent must independently produce its prediction without access to the future.

Record:

* Agent direction
* Agent predicted price/target
* Agent confidence
* Agent signal
* Bullish/bearish classification
* Reasoning
* Any recommended action
* Expected return

If the system has multiple agents, evaluate each agent separately as well as the combined decision.

---

# Step 4 — Reveal the Future

Only AFTER all forecasts and agent predictions have been permanently recorded, reveal the actual market data following the historical cutoff date.

Compare the predictions against what actually happened.

For example:

If the historical cutoff was 6 months ago, compare the prediction against the actual price and market behaviour during the following 6 months.

Do not alter or regenerate the original forecast after seeing the outcome.

---

# Step 5 — Measure Accuracy

Calculate objective performance metrics.

At minimum calculate:

### Directional Accuracy

Did the system correctly predict whether the asset would rise or fall?

Directional Accuracy = Correct Direction Predictions / Total Predictions × 100

### Price Prediction Error

Calculate:

* Absolute Error
* Percentage Error
* Mean Absolute Percentage Error (MAPE), where appropriate

### Return Prediction Accuracy

Compare:

Predicted Return vs Actual Return

Report:

* Predicted return
* Actual return
* Absolute difference
* Percentage difference

### Signal Accuracy

Evaluate whether the strength of the signal was justified by the subsequent market movement.

For example:

* Strong bullish signal → did the asset actually outperform?
* Strong bearish signal → did the asset actually decline?
* Neutral signal → did the asset remain relatively stable?

### Confidence Calibration

Compare confidence against actual success.

For example:

* 50–60% confidence → actual success rate
* 60–70% confidence → actual success rate
* 70–80% confidence → actual success rate
* 80–90% confidence → actual success rate
* 90–100% confidence → actual success rate

Determine whether high-confidence predictions are actually more accurate.

---

# Step 6 — Compare Forecast vs Agent

Evaluate the Forecast and Agent independently.

Create a comparison such as:

| Test Date | Forecast Direction | Actual Direction | Forecast Correct | Agent Direction | Agent Correct |
| --------- | ------------------ | ---------------- | ---------------- | --------------- | ------------- |

Then calculate:

* Forecast directional accuracy
* Agent directional accuracy
* Combined-system accuracy
* Average confidence
* Accuracy by confidence level
* Accuracy by signal strength

Determine whether the Agent adds predictive value beyond the Forecast system.

---

# Step 7 — Compare Predictions Against the Present

For each historical prediction, show what the prediction would have meant from the perspective of that historical date and compare it with what actually happened.

Example:

Historical date:
February 7, 2026

Price at prediction:
$100

Predicted 6-month target:
$120

Predicted return:
+20%

Actual price after 6 months:
$115

Actual return:
+15%

Prediction error:
5 percentage points

Directional prediction:
CORRECT

Price target:
OVERESTIMATED by $5

This comparison should be performed for every historical test.

---

# Step 8 — Identify Systematic Errors

Do not only report whether predictions were correct.

Look for systematic weaknesses.

Determine whether the system:

* Consistently overestimates upside
* Consistently underestimates downside
* Is too bullish
* Is too bearish
* Produces excessive confidence
* Performs poorly during high-volatility periods
* Performs poorly during market crashes
* Performs poorly around earnings
* Performs poorly during major news events
* Performs better on certain sectors or stocks
* Performs better at certain forecast horizons
* Produces unreliable predictions when the signal is weak

Identify recurring patterns.

---

# Step 9 — Produce an Overall Score

Create an overall validation report containing:

### Historical Test Summary

| Metric                          | Result |
| ------------------------------- | ------ |
| Number of historical tests      | X      |
| Directional accuracy            | X%     |
| Average return prediction error | X%     |
| Average price prediction error  | X%     |
| High-confidence accuracy        | X%     |
| Forecast accuracy               | X%     |
| Agent accuracy                  | X%     |
| Combined accuracy               | X%     |

Also report the results separately for each historical period.

---

# Step 10 — Compare Against a Baseline

Do NOT evaluate the system in isolation.

Compare it against simple baselines such as:

* Buy-and-hold
* Previous trend continuation
* Simple moving-average direction
* Random directional prediction (50%)
* Market/sector benchmark where appropriate

Determine whether the forecasting system actually provides predictive value beyond simple strategies.

---

# Important Validation Rules

1. Never use future information during prediction generation.
2. Never regenerate a historical prediction after seeing its outcome.
3. Clearly separate "prediction time" from "evaluation time."
4. Preserve the original prediction exactly as it was generated.
5. Calculate all technical indicators using only data available at the historical cutoff.
6. Treat each historical test as an independent simulation.
7. Do not cherry-pick successful predictions.
8. Report unsuccessful predictions with the same level of detail as successful ones.
9. If historical data is missing or uncertain, explicitly report it rather than filling the gap with current information.
10. If a metric cannot be calculated reliably, mark it as unavailable rather than estimating it.

---

# Final Deliverable

Produce a detailed historical validation report containing:

1. Executive summary
2. Methodology
3. Historical test dates
4. Information available at each cutoff
5. Original Forecast predictions
6. Original Agent predictions
7. Actual subsequent market outcomes
8. Forecast vs actual comparison
9. Agent vs actual comparison
10. Forecast vs Agent performance
11. Confidence calibration
12. Directional accuracy
13. Return prediction accuracy
14. Price-target accuracy
15. Baseline comparison
16. Systematic errors and weaknesses
17. Best-performing conditions
18. Worst-performing conditions
19. Overall performance score
20. Final assessment of whether the forecasting system demonstrates genuine predictive value

Most importantly, distinguish between:

**"The system predicted this correctly"**

and

**"The system predicted this correctly with a meaningful level of confidence and better performance than a simple baseline."**

The goal is not to make the system look successful. The goal is to determine objectively whether the forecasting system has genuine predictive power.
