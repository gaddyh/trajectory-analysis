| task | reward | pattern | failed_action_count | failed_write_count | failed_actions | arg_path | expected_value | actual_value | expected_refs | actual_refs | trace_pattern | arg_failure_type | contradiction_signal | execution_timing_signal | failed_assertions | communicate_info |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | 0.0 | ACTION_ONLY | 3 | 1 | get_product_details, get_order_details, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 28 | 0.0 | ACTION_ONLY | 1 | 0 | calculate | expression | 200.8 + 96.35 + 193.38 + 231.37 + 196.53 | 200.8 + 96.35 + 193.38 + 231.37 + 196... | 1 | 1 | EXPECTED_AND_ACTUAL_OBSERVED | UNKNOWN | - | - | - | 918.43 |
| 41 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | order_id | #W9583042 | #W4082615 | 59 | 64 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_ORDER_SELECTION | - | - | - | - |
| 2 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 10 |
| 57 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 20 | 0.0 | ACTION_ONLY | 3 | 1 | get_order_details, modify_pending_order_items, get_order_details | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 56 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['9534205511'] | ['9375701158'] | 16 | 18 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 3 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 6 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 18 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 0 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['7706410293', '7747408585'] | ['6342039236', '7747408585'] | 23 | 25 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 99 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 95 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | 167.87, 60.78, 107.09 |
| 1 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | item_ids | ['4983901480'] | ['1151293680', '4983901480'] | 16 | 23 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 72 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 47 | 0.0 | ACTION_ONLY | 4 | 0 | get_order_details, get_order_details, calculate, calculate | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 1095.55, 1528.14 |
| 76 | 0.0 | ACTION_ONLY | 1 | 1 | cancel_pending_order | reason | ordered by mistake | no longer needed | 11 | 15 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_REASON | - | - | - | 1939.05 |
| 27 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 82 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | item_ids | ['5952720925', '9973034634', '7381052... | ['6065192424'] | 27 | 21 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 4 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 10 |
| 36 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | $ | {'order_id': '#W9348897', 'item_ids':... |  | 22 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | camera, 481.5 |
| 64 | 0.0 | ACTION_ONLY | 2 | 2 | exchange_delivered_order_items, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 34 | 0.0 | ACTION_ONLY | 3 | 1 | get_order_details, get_order_details, modify_pending_order_address | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 1093.34 |
| 2 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 10 |
| 109 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | $ | {'order_id': '#W1603792', 'item_ids':... |  | 19 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | - |
| 106 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['2060066974'] | ['8124970213'] | 18 | 20 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 51 | 0.0 | ACTION_ONLY | 3 | 1 | get_product_details, get_order_details, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 100 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | payment_method_id | credit_card_3261838 | paypal_3650980 | 20 | 24 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_PAYMENT_METHOD | - | - | - | - |
| 28 | 0.0 | ACTION_ONLY | 1 | 0 | calculate | expression | 200.8 + 96.35 + 193.38 + 231.37 + 196.53 | 200.8 + 96.35 + 193.38 + 231.37 + 196... | 1 | 1 | EXPECTED_AND_ACTUAL_OBSERVED | UNKNOWN | - | - | - | 918.43 |
| 112 | 0.0 | ACTION_ONLY | 3 | 3 | modify_pending_order_items, modify_pending_order_address, modify_pending_orde... | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 104 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 286422338955 |
| 101 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | item_ids | ['3076708684'] | ['8886009523'] | 15 | 22 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 19 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | 54.04, 41.64 |
| 0 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['7706410293', '7747408585'] | ['6342039236', '7747408585'] | 21 | 23 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 20 | 0.0 | ACTION_ONLY | 7 | 1 | get_order_details, get_product_details, get_product_details, get_product_deta... | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 4 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 7 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 3 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 6 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 103 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | item_ids | ['4900661478', '3614853563'] | ['7824298782'] | 19 | 24 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | PREMATURE_TOOL_EXECUTION | - | 286422338955 |
| 41 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | order_id | #W9583042 | #W4082615 | 66 | 72 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_ORDER_SELECTION | - | - | - | - |
| 27 | 0.0 | ACTION_ONLY | 1 | 0 | get_order_details | order_id | #W3792453 | #W2575533 | 1 | 3 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_ORDER_SELECTION | - | - | - | - |
| 15 | 0.0 | ACTION_ONLY | 3 | 1 | get_order_details, get_order_details, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 5 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | $ | {'order_id': '#W6390527', 'item_ids':... |  | 18 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | - |
| 56 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['9534205511'] | ['9375701158'] | 16 | 18 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 110 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['2106335193'] | ['4913411651'] | 22 | 27 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 14 | 0.0 | ACTION_ONLY | 3 | 2 | get_order_details, return_delivered_order_items, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 18 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 72 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 74 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | payment_method_id | credit_card_4466831 | paypal_5914760 | 13 | 17 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_PAYMENT_METHOD | - | - | - | - |
| 79 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['2439754078'] | ['7661609223'] | 18 | 20 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 76 | 0.0 | ACTION_ONLY | 1 | 1 | cancel_pending_order | reason | ordered by mistake | no longer needed | 11 | 15 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_REASON | - | - | - | 1939.05 |
| 59 | 0.0 | ACTION_ONLY | 2 | 1 | calculate, cancel_pending_order | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 164.28, 625.60 |
| 34 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W1845024', 'address1':... |  | 33 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | 1093.34 |
| 71 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W5270061', 'address1':... |  | 39 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | - |
| 38 | 0.0 | ACTION_ONLY | 2 | 1 | calculate, cancel_pending_order | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | camera, 481.50 |
| 98 | 0.0 | ACTION_ONLY | 2 | 2 | exchange_delivered_order_items, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 95 | 0.0 | ACTION_ONLY | 2 | 2 | exchange_delivered_order_items, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 167.87, 60.78, 107.09 |
| 15 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | payment_method_id | paypal_5364164 | gift_card_1675628 | 18 | 16 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_PAYMENT_METHOD | - | - | - | - |
| 28 | 0.0 | ACTION_ONLY | 1 | 0 | calculate | expression | 200.8 + 96.35 + 193.38 + 231.37 + 196.53 | 200.80 + 96.35 + 193.38 + 231.37 + 19... | 0 | 1 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | UNKNOWN | - | - | - | 918.43 |
| 25 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 4 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 7 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 82 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | item_ids | ['5952720925', '9973034634', '7381052... | ['6065192424'] | 24 | 18 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 2 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 10 |
| 0 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['7706410293', '7747408585'] | ['6342039236', '7747408585'] | 23 | 25 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 99 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 110 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['2106335193'] | ['4913411651'] | 20 | 23 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 37 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | item_ids | ['6117189161', '7453605304', '3799046... | ['6117189161', '9879255677', '7453605... | 46 | 68 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | camera, 481.50 |
| 107 | 0.0 | ACTION_AND_NL | 1 | 1 | exchange_delivered_order_items | item_ids | ['1615379700'] | ['6245746168'] | 25 | 27 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | Agent should exchange items in both orders. | - |
| 3 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 6 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 100 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_items, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 51 | 0.0 | ACTION_ONLY | 3 | 1 | get_product_details, get_order_details, return_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 21 | 0.0 | ACTION_ONLY | 5 | 1 | get_product_details, get_product_details, get_product_details, calculate, mod... | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 44.08 |
| 20 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['4579334072', '1151293680', '4107812... | ['4579334072', '1151293680', '4153505... | 36 | 42 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 36 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | item_ids | ['6117189161', '7453605304', '3799046... | ['6117189161'] | 46 | 21 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | camera, 481.5 |
| 45 | 0.0 | ACTION_ONLY | 2 | 1 | calculate, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 9.89 |
| 59 | 0.0 | ACTION_ONLY | 3 | 2 | calculate, cancel_pending_order, modify_pending_order_address | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 164.28, 625.60 |
| 27 | 0.0 | ACTION_ONLY | 1 | 0 | get_order_details | order_id | #W3792453 | #W5565470 | 1 | 3 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_ORDER_SELECTION | - | - | - | - |
| 43 | 0.0 | ACTION_ONLY | 1 | 1 | modify_user_address | address1 | 943 Maple Drive | 1842 W Belmont Ave | 48 | 66 | EXPECTED_AND_ACTUAL_OBSERVED | UNKNOWN | - | - | - | 840887978435, 943 Maple Drive, Suite 356, Chicago, IL, 60621, 64GB |
| 82 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | item_ids | ['5952720925', '9973034634', '7381052... | ['8551474201'] | 2 | 16 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 41 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | order_id | #W9583042 | #W4082615 | 62 | 65 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_ORDER_SELECTION | - | - | - | - |
| 72 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 105 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 99 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 74 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | payment_method_id | credit_card_4466831 | paypal_5914760 | 19 | 23 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_PAYMENT_METHOD | - | - | - | - |
| 2 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 5 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 76 | 0.0 | ACTION_ONLY | 1 | 1 | cancel_pending_order | reason | ordered by mistake | no longer needed | 14 | 18 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_REASON | - | - | - | 1939.05 |
| 4 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 7 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 0 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['7706410293', '7747408585'] | ['6342039236', '7747408585'] | 25 | 27 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 34 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W1845024', 'address1':... |  | 37 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | 1093.34 |
| 94 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | item_ids | ['3478699712'] | ['2216662955'] | 11 | 18 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 95 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | 167.87, 60.78, 107.09 |
| 3 | 0.0 | ACTION_ONLY | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 6 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | WRONG_PRODUCT_LOOKUP | - | - | - | 10 |
| 112 | 0.0 | ACTION_ONLY | 3 | 3 | modify_pending_order_items, modify_pending_order_address, modify_pending_orde... | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 28 | 0.0 | ACTION_ONLY | 1 | 0 | calculate | $ | {'expression': '200.8 + 96.35 + 193.3... |  | 0 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | 918.43 |
| 109 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['2106335193'] | ['4913411651'] | 27 | 31 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 18 | 0.0 | ACTION_ONLY | 2 | 1 | get_product_details, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 100 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | $ | {'order_id': '#W8488728', 'item_ids':... |  | 10 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | - |
| 27 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 43 | 0.0 | ACTION_ONLY | 2 | 1 | get_order_details, modify_user_address | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 840887978435, 943 Maple Drive, Suite 356, Chicago, IL, 60621, 64GB |
| 80 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 34 | 0.0 | ACTION_ONLY | 3 | 1 | get_order_details, get_order_details, modify_pending_order_address | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 1093.34 |
| 62 | 0.0 | ACTION_ONLY | 2 | 0 | get_order_details, get_product_details | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 302.67, 20 hours |
| 39 | 0.0 | ACTION_ONLY | 3 | 1 | find_user_id_by_name_zip, get_order_details, modify_user_address | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 46.66 |
| 101 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W4219264', 'address1':... |  | 18 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | - |
| 20 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['4579334072', '1151293680', '4107812... | ['4579334072', '1151293680', '4153505... | 36 | 42 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 92 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | item_ids | ['9494281769'] | ['4545791457', '3098764622', '1631806... | 5 | 20 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 59 | 0.0 | ACTION_ONLY | 3 | 2 | calculate, cancel_pending_order, modify_pending_order_address | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | 164.28, 625.60 |
| 79 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['2439754078'] | ['7661609223'] | 19 | 21 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 72 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 91 | 0.0 | ACTION_ONLY | 2 | 2 | return_delivered_order_items, exchange_delivered_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 56 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['9534205511'] | ['9375701158'] | 17 | 20 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 64 | 0.0 | ACTION_ONLY | 2 | 2 | exchange_delivered_order_items, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 82 | 0.0 | ACTION_ONLY | 1 | 1 | return_delivered_order_items | item_ids | ['5952720925', '9973034634', '7381052... | ['6065192424'] | 28 | 22 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | - |
| 107 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['3112842858'] | ['4572024853'] | 22 | 26 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_VARIANT_SELECTION | - | - | - | - |
| 101 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W4219264', 'address1':... |  | 29 | 0 | MISSING_ACTUAL_CALL | MISSING_ACTION | - | - | - | - |
| 99 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | UNKNOWN | - | - | - | - |
| 110 | 0.0 | ACTION_ONLY | 3 | 3 | modify_pending_order_address, modify_user_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 111 | 0.0 | ACTION_AND_NL | 3 | 3 | modify_pending_order_items, modify_pending_order_address, modify_pending_orde... | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | Agent should modify the items and address as requested. | - |
| 112 | 0.0 | ACTION_ONLY | 2 | 2 | modify_pending_order_address, modify_pending_order_items | - | - | - | - | - | - | MULTI_FAILED_ACTIONS | - | - | - | - |
| 36 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | item_ids | ['6117189161', '7453605304', '3799046... | ['6117189161'] | 58 | 29 | EXPECTED_AND_ACTUAL_OBSERVED | WRONG_SOURCE_ITEM_SELECTION | - | - | - | camera, 481.5 |

## Failure Type Distribution

| failure_type | count | pct |
| --- | --- | --- |
| UNKNOWN | 17 | 22.4% |
| WRONG_VARIANT_SELECTION | 16 | 21.1% |
| WRONG_SOURCE_ITEM_SELECTION | 13 | 17.1% |
| MISSING_ACTION | 10 | 13.2% |
| WRONG_PRODUCT_LOOKUP | 8 | 10.5% |
| WRONG_ORDER_SELECTION | 5 | 6.6% |
| WRONG_PAYMENT_METHOD | 4 | 5.3% |
| WRONG_REASON | 3 | 3.9% |

## Trace Pattern Distribution

| failure_type | count | pct |
| --- | --- | --- |
| EXPECTED_AND_ACTUAL_OBSERVED | 44 | 69.8% |
| MISSING_ACTUAL_CALL | 10 | 15.9% |
| EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | 9 | 14.3% |
