# Remarks — Session 1

Date: June 2026

## Objective

The original goal was to compare expected and observed trajectories in Tau2 and determine where an agent diverged from the benchmark reference path.

During implementation, a more important insight emerged: trajectory divergence and benchmark failure are not the same thing.

---

## Key Discovery #1 — Reward Is Not a Diagnosis

Initially, the assumption was:

```text
Reward = 0
→ Agent failed
```

Task 2 demonstrated that this assumption is insufficient.

The benchmark reward was:

```text
DB = 1.0
NL_ASSERTION = 0.0
Reward = 0.0
```

The database mutation succeeded.

The communication requirement failed.

The benchmark outcome alone did not explain the failure.

This motivated explicit reward-channel analysis.

---

## Key Discovery #2 — Reward Channels Are Behavioral Signals

Tau2 exposes multiple evaluation channels.

Example:

```text
DB
NL_ASSERTION
```

These channels provide substantially more information than a single reward value.

A run may:

```text
Pass DB
Fail NL_ASSERTION
```

or

```text
Pass NL_ASSERTION
Fail DB
```

These represent fundamentally different failure modes.

Future analysis should treat reward channels as independent behavioral dimensions.

---

## Key Discovery #3 — Expected Trajectories Are Not Ground Truth

Several runs revealed that agents can follow alternative information-gathering paths.

Example:

Expected:

```text
get_product_details(...)
```

Actual:

```text
list_all_product_types(...)
get_product_details(...)
```

The actual trajectory diverged from the reference trajectory but still gathered relevant information.

This suggests that:

```text
Trajectory Divergence
≠
Task Failure
```

Expected trajectories should therefore be interpreted as reference behaviors rather than mandatory execution paths.

---

## Key Discovery #4 — Communication Is a First-Class Failure Mode

Task 2 produced:

```text
DB = 1.0
NL_ASSERTION = 0.0
```

The agent successfully executed the return.

However, it communicated:

```text
12 t-shirt options
```

instead of:

```text
10 available t-shirt options
```

The environment state was correct.

The user-facing answer was incorrect.

This demonstrates that communication failures can exist independently of tool-use failures.

---

## Key Discovery #5 — Failure Localization Is More Useful Than Outcome Evaluation

The initial project focused on:

```text
Success
Failure
```

The project now focuses on:

```text
Failure Channel
↓
Root Cause
↓
Impact
↓
Evidence
```

This transformation makes benchmark results actionable.

Instead of asking:

```text
Did the agent fail?
```

we can ask:

```text
Why did it fail?
```

and

```text
What specifically should be improved?
```

---

## Key Discovery #6 — Deterministic Diagnosis Is Possible

The current report generation does not require an LLM.

Using only benchmark metadata, trajectory comparison, reward breakdowns, and assertion results, the system can generate:

* Failure Channel
* Primary Failure
* Root Cause
* Impact
* Supporting Evidence

This suggests that a large portion of agent failure analysis may be performed deterministically before introducing model-based judges.

---

## Current Pipeline

```text
Task
↓
Explain Task
↓
Extract Trajectory
↓
Compare Expected vs Actual
↓
Reward Breakdown
↓
Failure Channel
↓
Diagnosis
↓
Root Cause
↓
Trajectory Report
```

---

## Next Milestone

Move from single-run analysis to dataset analysis.

Target:

```text
100 simulations
↓
100 trajectory reports
↓
Failure distributions
↓
Reward-channel distributions
↓
Failure hotspots
↓
Representative examples
```

The next objective is to determine whether consistent behavioral structures emerge across the benchmark.

Examples:

* Communication pressure
* Grounding pressure
* Planning pressure
* Retrieval pressure
* Argument-selection pressure

These should emerge from the data rather than being imposed beforehand.

---

## Working Hypothesis

Outcome metrics answer:

```text
Did the agent succeed?
```

Reward channels answer:

```text
Where did it fail?
```

Trajectory analysis answers:

```text
How did it fail?
```

Failure reports answer:

```text
What should be improved?
```
