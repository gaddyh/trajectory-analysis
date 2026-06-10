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

The goal is to evaluate agent behavior.

---

# Core Question

Can trajectory analysis explain agent failures better than outcome metrics alone?

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

System:

User
→ Agent
→ Tools
→ Environment
→ Outcome

The entire system is the unit of evaluation.

---

## Step 2: Define the Task

Each Tau2 task defines:

* User objective
* Expected actions
* Environment constraints
* Success criteria

Example:

Exchange a delivered keyboard and thermostat for different variants.

Success is defined by the benchmark.

---

## Step 3: Capture the Trajectory

A trajectory is the sequence of actions taken by the agent.

Example:

Authenticate User
→ Retrieve Order
→ Retrieve Product
→ Clarify Preferences
→ Execute Exchange

Trajectory analysis focuses on this sequence rather than only the final outcome.

---

## Step 4: Observe Behavior

For every trajectory we collect:

* Messages
* Tool calls
* Tool arguments
* Tool outputs
* State changes
* Final reward

This produces a complete behavioral trace.

---

## Step 5: Localize Failures

Instead of asking:

"Did the task fail?"

We ask:

"Where did the trajectory diverge from expected behavior?"

Example:

Authentication ✓

Order Retrieval ✓

Product Retrieval ✓

Clarification ✓

Exchange Tool ✓

Variant Selection ✗

This converts a binary failure into an explainable failure.

---

## Step 6: Build a Failure Taxonomy

Every failure should be assigned to a behavioral category.

Initial taxonomy:

* Authentication Failure
* Retrieval Failure
* Grounding Failure
* Clarification Failure
* Planning Failure
* Tool Selection Failure
* Argument Selection Failure
* State Transition Failure

The taxonomy should evolve as new failure modes are discovered.

---

## Step 7: Define Metrics

### Outcome Metrics

* Reward
* Success Rate

### Trajectory Metrics

* Action Recall
* Action Precision
* Tool Selection Accuracy
* Argument Accuracy
* State Transition Accuracy
* Trajectory Length
* Read / Write Ratio
* Confirmation Before Action

### Failure Metrics

* Failure Type Distribution
* Failure Location Distribution
* Failure Severity

---

## Step 8: Generate Trajectory Reports

For every simulation:

Output:

TrajectoryReport

Example:

{
"success": false,
"reward": 0.0,
"failure_type": "argument_selection",
"failure_location": "exchange_delivered_order_items",
"summary": "Selected incorrect keyboard variant after successful retrieval and clarification."
}

The report should explain the failure in human-readable language.

---

## Step 9: Aggregate Across the Dataset

Run the evaluator across 100 simulations.

Compute:

* Failure Frequency
* Failure Distribution
* Common Failure Paths
* Failure Hotspots

Example:

Grounding: 34%

Argument Selection: 29%

Planning: 18%

Tool Selection: 11%

Other: 8%

The goal is to understand where failures cluster.

---

## Step 10: Discover Behavioral Structure

Only after analyzing failure distributions should higher-level theories be introduced.

Possible examples:

* Grounding Pressure
* Planning Pressure
* Clarification Pressure
* State Tracking Pressure

These are hypotheses that emerge from the data.

They are not assumptions.

---

# Deliverables

## Per-Run Report

TrajectoryReport

Human-readable explanation of:

* What happened
* Where divergence occurred
* Which failure type was responsible

---

## Dataset Report

TrajectoryAnalysisReport

Includes:

* Success Rate
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

Trajectory analysis tells us why.
