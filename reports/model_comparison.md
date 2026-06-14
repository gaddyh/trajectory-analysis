
## Model Comparison — Failure Type Breakdown

| model | tasks | pass_rate | failed | variant | source_item | product | order | payment | reason | missing | multi | unknown | localized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| claude-3-7-sonnet-20250219 | 456 | 79% | 97 | 13 (13%) | 17 (18%) | 3 (3%) | 3 (3%) | 1 (1%) | 4 (4%) | 8 (8%) | 27 (28%) | 21 (22%) | 49 (51%) |
| gpt-4.1-2025-04-14 | 456 | 74% | 118 | 16 (14%) | 13 (11%) | 8 (7%) | 5 (4%) | 4 (3%) | 3 (3%) | 10 (8%) | 42 (36%) | 17 (14%) | 59 (50%) |
| gpt-4.1-mini-2025-04-14 | 456 | 66% | 155 | 23 (15%) | 16 (10%) | 9 (6%) | 3 (2%) | 2 (1%) | 1 (1%) | 25 (16%) | 55 (35%) | 21 (14%) | 79 (51%) |
| o4-mini-2025-04-16 | 456 | 71% | 130 | 15 (12%) | 19 (15%) | 0 (0%) | 5 (4%) | 1 (1%) | 2 (2%) | 12 (9%) | 65 (50%) | 11 (8%) | 54 (42%) |

## Model Comparison — Trace Pattern Breakdown

| model | expected+actual | expected_missing | missing_call |
| --- | --- | --- | --- |
| claude-3-7-sonnet-20250219 | 38 (39%) | 7 (7%) | 8 (8%) |
| gpt-4.1-2025-04-14 | 44 (37%) | 9 (8%) | 10 (8%) |
| gpt-4.1-mini-2025-04-14 | 48 (31%) | 9 (6%) | 25 (16%) |
| o4-mini-2025-04-16 | 43 (33%) | 0 (0%) | 12 (9%) |

## Legend

Failure type % = count / failed_tasks

- `variant` = WRONG_VARIANT_SELECTION
- `source_item` = WRONG_SOURCE_ITEM_SELECTION
- `product` = WRONG_PRODUCT_LOOKUP
- `order` = WRONG_ORDER_SELECTION
- `payment` = WRONG_PAYMENT_METHOD
- `reason` = WRONG_REASON
- `missing` = MISSING_ACTION
- `multi` = MULTI_FAILED_ACTIONS
- `unknown` = UNKNOWN
- `localized` = failed - multi - unknown (arg-level localizer coverage)

Trace pattern % = count / failed_tasks

- `expected+actual` = EXPECTED_AND_ACTUAL_OBSERVED
- `expected_missing` = EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED
- `missing_call` = MISSING_ACTUAL_CALL
