# Remarks – Dataset-Level Findings (Retail 100)

Date: June 2026

## Context

Today we moved from per-run trajectory analysis to dataset-level analysis.

The evaluator was executed on:

```text
baseline_retail_100
```

and produced both per-task diagnostics and aggregate statistics.

This was the first opportunity to evaluate whether the trajectory-analysis framework can surface behavioral structure that is not visible from benchmark reward alone.

---

# Key Findings

## 1. Database Failures Dominate

Failure distribution:

```text
database_state: 17
database_and_communication: 4
communication: 2
```

Reward-channel view:

```text
DB failures: 21
NL failures: 6
```

Observation:

Most failures involve database state rather than communication.

This suggests that the dominant reliability bottleneck in this benchmark slice is execution correctness rather than user communication.

---

## 2. Communication Failures Exist but Are Rare

Only six tasks involved NL assertion failures.

Examples include:

```text
Expected:
"There are 10 available t-shirt options."

Actual:
"There are 12 t-shirt options."
```

The agent successfully completed the database operation but communicated incorrect information to the user.

Observation:

Communication failures are meaningful but represent a minority of overall failures.

---

## 3. Fidelity Is Not Strongly Coupled To Success

Dataset summary:

```text
Successful runs with fidelity < 100%:
28
```

Observation:

Many successful trajectories diverge substantially from the benchmark reference trajectory.

Implication:

```text
Reference trajectory
≠
Required trajectory
```

The benchmark trajectory should therefore be interpreted as one valid behavioral path rather than the only valid path.

This is one of the most important findings so far.

---

## 4. Perfect Fidelity Does Not Guarantee Success

Dataset summary:

```text
Failed runs with fidelity = 100%:
7
```

Observation:

Some runs matched the expected trajectory but still failed.

Possible explanations:

* Hidden state mismatch
* Communication failure
* Incomplete trajectory specification
* Benchmark limitations
* Fidelity metric too coarse

These cases are especially valuable because they reveal disagreement between trajectory matching and benchmark reward.

Future analysis should prioritize these examples.

---

## 5. Agents Routinely Take Alternative Paths

Dataset summary:

```text
Total extra actions: 367
Total missing actions: 84
```

Observation:

Agents frequently gather additional information or skip expected reads while still achieving successful outcomes.

Example:

```text
Expected:
get_product_details(...)

Actual:
list_all_product_types(...)
```

This reinforces the idea that reward and trajectory are related but distinct behavioral dimensions.

---

## 6. Reward Channels Improve Failure Localization

Traditional benchmark output:

```text
Reward = 0
```

Trajectory-analysis output:

```text
DB = 1
NL_ASSERTION = 0
```

or

```text
DB = 0
NL_ASSERTION = 1
```

or

```text
DB = 0
NL_ASSERTION = 0
```

Observation:

Reward decomposition dramatically improves diagnosability.

Instead of knowing only that a task failed, we can identify which behavioral channel failed.

---

## 7. Trajectory Reports Are Producing Actionable Diagnoses

Current reports provide:

* Outcome
* Reward breakdown
* Failure channel
* Root cause
* Impact
* Trajectory variation

Example:

```text
FAIL — communication failure.

Database action succeeded,
but required information `10`
was not communicated.
```

This is substantially more informative than benchmark reward alone.

---

# Methodological Insight

The project originally focused on trajectory comparison.

However, today's results suggest that reward-channel decomposition may be equally important.

Current workflow:

```text
Reward
→ Reward Channels
→ Trajectory Comparison
→ Failure Diagnosis
```

This creates a deterministic explanation pipeline.

---

# Proposed Next Metrics

## Read Fidelity

```text
matched_reads / expected_reads
```

Example:

```text
3 / 5 = 60%
```

---

## Write Fidelity

```text
matched_writes / expected_writes
```

Example:

```text
1 / 1 = 100%
```

Observation:

Read behavior and write behavior represent different cognitive demands and should not be merged into a single fidelity metric.

---

## Execution Efficiency

```text
expected_actions / actual_actions
```

Example:

```text
expected = 5
actual = 10

efficiency = 50%
```

This separates:

```text
Correct and efficient
```

from

```text
Correct but expensive
```

behavior.

---

# Most Important Next Investigation

Analyze:

```text
Failed runs with fidelity = 100%
```

These are the most informative cases in the dataset because:

* The benchmark says failure.
* The trajectory says success.

Understanding these disagreements may reveal:

* Hidden behavioral constraints
* Weaknesses in the fidelity metric
* Benchmark inconsistencies
* New failure categories

---

# Current Conclusion

Trajectory analysis is already revealing behavioral structure that is invisible from reward alone.

The strongest findings so far are:

1. Database-state failures dominate.
2. Communication failures are relatively rare.
3. Success does not require strict trajectory adherence.
4. Perfect trajectory fidelity does not guarantee success.
5. Reward-channel decomposition substantially improves failure diagnosis.

The framework is beginning to transition from a debugging tool into a behavioral evaluation framework.
