# Trajectory Analysis for Agent Reliability

## Motivation

Most agent benchmarks report a single outcome metric:

* Reward
* Success Rate
* Pass / Fail

While useful, outcome metrics alone do not explain why an agent succeeds or fails.

A task with reward = 0 may contain a nearly correct trajectory with a single incorrect decision.

A task with reward = 1 may contain inefficient, fragile, or unsafe behavior.

Inspired by recent work on AI evaluation and trajectory analysis, this project aims to move beyond outcome evaluation and toward behavioral evaluation.

The goal is not to evaluate prompts.

The goal is to evaluate observable agent behavior.

---

## Current Status

Implemented:

- Tau2 task loading
- Expected vs observed trajectory extraction
- Action matching
- Argument matching
- Missing action detection
- Extra action detection
- Reward breakdown analysis
- Failure channel diagnosis
- Deterministic trajectory reports

Current reports explain:

- Outcome
- Reward breakdown
- Primary failure channel
- Root cause
- Impact
- Trajectory divergence

Next milestone:

- Dataset-wide aggregation across 100 simulations
- Failure distributions
- Failure hotspots
- Representative failure examples

---

# Core Question

Can trajectory analysis and reward-channel analysis explain agent failures better than outcome metrics alone?

---

# Dataset

We use the Tau2 benchmark.

Tau2 is particularly useful because it provides:

* Task definitions
* Expected actions
* Tool calls
* Tool outputs
* Environment state
* Final reward
* Reward breakdowns
* Natural language assertions

This allows us to compare:

Expected Trajectory

against

Observed Trajectory

for every task.

---

# Methodology

## Step 1: Define the System Boundary

We do not evaluate a prompt.

We evaluate an agent system.

```text
User
→ Agent
→ Tools
→ Environment
→ Outcome
```

The entire system is the unit of evaluation.

---

## Step 2: Define the Task

Each Tau2 task defines:

* User objective
* Expected actions
* Environment constraints
* Success criteria
* Communication requirements

Example:

```text
Exchange a delivered keyboard and thermostat
for different variants.
```

Success is defined by the benchmark.

---

## Step 3: Capture the Trajectory

A trajectory is the sequence of actions taken by the agent.

Example:

```text
Authenticate User
→ Retrieve Order
→ Retrieve Product
→ Clarify Preferences
→ Execute Exchange
```

Trajectory analysis focuses on this sequence rather than only the final outcome.

---

## Step 4: Observe Behavior

For every trajectory we collect:

* Messages
* Tool calls
* Tool arguments
* Tool outputs
* State changes
* Reward signals

This produces a complete behavioral trace.

---

## Step 5: Separate Outcome From Explanation

A reward tells us whether a run passed.

It does not tell us why.

Example:

```text
Reward = 0.0
```

This alone is not actionable.

Instead we decompose the outcome into reward channels.

Example:

```text
DB = 1.0
NL_ASSERTION = 0.0
Reward = 0.0
```

This reveals that the database mutation succeeded while the communication requirement failed.

---

## Step 6: Localize Failures

Instead of asking:

```text
Did the task fail?
```

We ask:

```text
Why did the task fail?
```

Example:

```text
Authentication ✓
Order Retrieval ✓
Product Retrieval ✓
Exchange ✓
Communication ✗
```

This converts a binary failure into an explainable failure.

---

## Step 7: Build a Failure Taxonomy

Every failure should be assigned to a behavioral category.

Current taxonomy:

### Communication Failure

Required information was not communicated correctly.

Example:

```text
Expected:
"There are 10 available t-shirt options."

Actual:
"There are 12 t-shirt options."
```

### Retrieval Failure

Required information was never collected.

### Grounding Failure

Information was collected but interpreted incorrectly.

### Tool Selection Failure

The wrong tool was selected.

### Argument Selection Failure

The correct tool was selected with incorrect arguments.

### State Transition Failure

The final environment state did not match expectations.

### Trajectory Divergence

The agent followed an alternative information-gathering strategy.

Example:

```text
Expected:
get_product_details(...)

Actual:
list_all_product_types(...)
```

Trajectory divergence may or may not affect reward.

The taxonomy should evolve as new failure modes are discovered.

---

## Step 8: Define Metrics

### Outcome Metrics

* Reward
* Success Rate

### Reward Diagnostics

* Reward Breakdown
* DB Pass Rate
* NL Assertion Pass Rate

### Trajectory Metrics

* Action Recall
* Action Precision
* Tool Selection Accuracy
* Argument Accuracy
* Trajectory Length
* Read / Write Ratio
* Extra Actions
* Missing Actions

### Failure Metrics

* Failure Type Distribution
* Failure Location Distribution
* Failure Severity

---

## Step 9: Generate Trajectory Reports

For every simulation we generate a deterministic TrajectoryReport.

Example:

```json
{
  "success": false,
  "reward": 0.0,
  "reward_breakdown": {
    "DB": 1.0,
    "NL_ASSERTION": 0.0
  },
  "failure_channel": "NL_ASSERTION",
  "primary_failure": "communication",
  "root_cause": "Required information `10` was not communicated.",
  "impact": "Database state was correct, but communication failed."
}
```

The report should explain:

* What happened
* Why it failed
* Which reward channel failed
* Whether trajectory divergence occurred

---

## Step 10: Aggregate Across the Dataset

Run the evaluator across a benchmark slice.

Compute:

* Success Rate
* Failure Distribution
* Reward Channel Distribution
* Common Failure Paths
* Failure Hotspots

Example:

```text
Communication: 34%

Argument Selection: 29%

Grounding: 18%

Tool Selection: 11%

Other: 8%
```

The goal is to understand where failures cluster.

---

## Step 11: Discover Behavioral Structure

Only after analyzing failure distributions should higher-level theories be introduced.

Possible examples:

* Grounding Pressure
* Planning Pressure
* Clarification Pressure
* State Tracking Pressure
* Communication Pressure

These are hypotheses that emerge from the data.

They are not assumptions.

---

# Deliverables

## Per-Run Report

TrajectoryReport

Human-readable explanation of:

* Outcome
* Reward Breakdown
* Primary Failure Channel
* Root Cause
* Impact
* Supporting Evidence

---

## Dataset Report

TrajectoryAnalysisReport

Includes:

* Success Rate
* Reward Breakdown Statistics
* Failure Distribution
* Failure Heatmaps
* Failure Examples
* Representative Trajectories

---

# Non-Goals

This project is not:

* Prompt engineering
* Prompt optimization
* Agent architecture research

The purpose is evaluation.

We aim to understand agent behavior before attempting to improve it.

---

# Guiding Principle

Outcome metrics tell us whether an agent succeeded.

Reward breakdowns tell us where success or failure occurred.

Trajectory analysis helps explain why.

Failure reports turn benchmark results into actionable engineering insights.
