# Trajectory Analysis

Deterministic Failure Localization for Tool-Using Agents

## Overview

Most agent benchmarks produce a single outcome metric:

* Reward
* Success Rate
* Pass / Fail

These metrics tell us whether an agent succeeded.

They do not explain why.

Tau2 is unusual because it exposes rich evaluation artifacts:

* Expected actions
* Actual tool calls
* Action checks
* Argument mismatches
* Tool outputs
* Environment state
* Natural-language assertions
* Reward breakdowns

This project converts those artifacts into deterministic behavioral diagnostics.

Instead of stopping at:

```text
Reward = 0
```

we localize failures to:

```text
Failed Action
→ Argument Mismatch
→ Trace Evidence
→ Failure Category
```

without using an LLM judge.

The goal is to transform benchmark outputs into actionable engineering signals.

---

## Example

A benchmark result might only tell us:

```text
Reward = 0
```

Trajectory Analysis produces:

```text
Task: 74

Failed Action:
modify_pending_order_items

Argument Mismatch:
payment_method_id

Expected:
credit_card_4466831

Actual:
paypal_5914760

Failure Type:
WRONG_PAYMENT_METHOD

Trace Pattern:
EXPECTED_AND_ACTUAL_OBSERVED
```

The benchmark says the task failed.

The analyzer explains why.

---

## Failure Localization

For single-action failures, the framework extracts:

* Failed action
* Argument path
* Expected value
* Actual value
* Evidence locations inside the trajectory
* Failure category

Example:

| task | failed_action                | arg_path          | expected            | actual           | failure_type          |
| ---- | ---------------------------- | ----------------- | ------------------- | ---------------- | --------------------- |
| 41   | modify_pending_order_address | order_id          | #W9583042           | #W4082615        | WRONG_ORDER_SELECTION |
| 74   | modify_pending_order_items   | payment_method_id | credit_card_4466831 | paypal_5914760   | WRONG_PAYMENT_METHOD  |
| 76   | cancel_pending_order         | reason            | ordered by mistake  | no longer needed | WRONG_REASON          |

---

## Failure Taxonomy

Current deterministic taxonomy:

| Failure Type                | Description                                     |
| --------------------------- | ----------------------------------------------- |
| WRONG_VARIANT_SELECTION     | Wrong replacement variant selected              |
| WRONG_SOURCE_ITEM_SELECTION | Wrong source item chosen                        |
| WRONG_PRODUCT_LOOKUP        | Wrong product retrieved                         |
| WRONG_ORDER_SELECTION       | Wrong order selected                            |
| WRONG_PAYMENT_METHOD        | Wrong payment method used                       |
| WRONG_REASON                | Incorrect cancellation reason                   |
| MISSING_ACTION              | Expected action never executed                  |
| MULTI_FAILED_ACTIONS        | Multiple failed actions require deeper analysis |
| UNKNOWN                     | Failure could not be localized                  |

---

## Trace Patterns

The framework also classifies where the failure originated.

### EXPECTED_AND_ACTUAL_OBSERVED

Both values existed in context.

The model selected the wrong one.

Example:

```text
Correct order visible
Wrong order visible

Model chose wrong order.
```

### EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED

Correct value never appeared in the trajectory.

The model grounded on incomplete information.

### MISSING_ACTUAL_CALL

The expected action never occurred.

---

## Cross-Model Analysis

The framework can compare behavioral failure distributions across models.

### Failure Type Breakdown

| model             | pass_rate | failed | variant | source_item | product | order | payment | reason | missing | multi |
| ----------------- | --------- | ------ | ------- | ----------- | ------- | ----- | ------- | ------ | ------- | ----- |
| Claude 3.7 Sonnet | 79%       | 97     | 13%     | 18%         | 3%      | 3%    | 1%      | 4%     | 8%      | 28%   |
| GPT-4.1           | 74%       | 118    | 14%     | 11%         | 7%      | 4%    | 3%      | 3%     | 8%      | 36%   |
| GPT-4.1 Mini      | 66%       | 155    | 15%     | 10%         | 6%      | 2%    | 1%      | 1%     | 16%     | 35%   |
| o4-mini           | 71%       | 130    | 12%     | 15%         | 0%      | 4%    | 1%      | 2%     | 9%      | 50%   |

### Trace Pattern Breakdown

| model             | expected+actual | expected_missing | missing_call |
| ----------------- | --------------- | ---------------- | ------------ |
| Claude 3.7 Sonnet | 39%             | 7%               | 8%           |
| GPT-4.1           | 37%             | 8%               | 8%           |
| GPT-4.1 Mini      | 31%             | 6%               | 16%          |
| o4-mini           | 33%             | 0%               | 9%           |

---

## Current Findings

Across multiple Tau2 retail runs:

* Roughly 50% of failures can be localized deterministically to an argument-level mismatch.
* The most common localized failures are:

  * Variant selection
  * Source item selection
  * Missing actions
* A large remaining bucket consists of multi-action failures that require deeper decomposition.
* Many failures occur despite the correct answer appearing in the trajectory, suggesting selection errors rather than retrieval failures.

---

## Usage

Analyze a benchmark file:

```bash
python scripts/inspect_tau2_failures.py \
  results.json \
  --failed-only \
  --table
```

Generate markdown reports:

```bash
python scripts/inspect_tau2_failures.py \
  results.json \
  --failed-only \
  --table \
  --md-out report.md
```

Compare multiple models:

```bash
python scripts/compare_models.py \
  data/raw/simulations \
  --domain retail
```

---

## Why This Exists

Benchmarks are usually used for ranking models.

This project treats benchmark outputs as behavioral datasets.

Instead of asking:

```text
Did the agent fail?
```

we ask:

```text
Which action failed?

Which argument was wrong?

Where did that value originate?

What category of failure is this?
```

The objective is not leaderboard optimization.

The objective is failure understanding.
