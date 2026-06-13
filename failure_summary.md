| task | reward | pattern | failed_action_count | failed_write_count | failed_actions | arg_path | expected_value | actual_value | expected_refs | actual_refs | trace_pattern | failed_assertions | communicate_info |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.0 | ACTION_AND_NL | 2 | 1 | get_product_details, return_delivered_order_items | - | - | - | - | - | - | Agent should tell the user that there are 10 t-shirt options available. | 10 |
| 0 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['7706410293', '7747408585'] | ['6342039236', '7747408585'] | 25 | 27 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
| 3 | 0.0 | ACTION_AND_NL | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 6 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | Agent should tell the user that there are 10 t-shirt options available. | 10 |
| 4 | 0.0 | ACTION_AND_NL | 1 | 0 | get_product_details | product_id | 6086499569 | 9523456873 | 0 | 7 | EXPECTED_NOT_OBSERVED_ACTUAL_OBSERVED | Agent should tell the user that there are 10 t-shirt options available. | 10 |
| 19 | 0.0 | ACTION_AND_NL | 1 | 1 | return_delivered_order_items | $ | {'order_id': '#W2890441', 'item_ids':... |  | 12 | 0 | MISSING_ACTUAL_CALL | Agent should tell the user that exchanging the pet bed and office chair saves... | 54.04, 41.64 |
| 20 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['4579334072', '1151293680', '4107812... | ['4579334072', '1151293680', '4153505... | 43 | 51 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
| 37 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | item_ids | ['6117189161', '7453605304', '3799046... | ['6117189161', '9879255677', '7453605... | 38 | 56 | EXPECTED_AND_ACTUAL_OBSERVED | - | camera, 481.50 |
| 36 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | item_ids | ['6117189161', '7453605304', '3799046... | ['6117189161', '9879255677', '7453605... | 47 | 69 | EXPECTED_AND_ACTUAL_OBSERVED | - | camera, 481.5 |
| 38 | 0.0 | ACTION_ONLY | 2 | 1 | calculate, cancel_pending_order | - | - | - | - | - | - | - | camera, 481.50 |
| 39 | 0.0 | ACTION_ONLY | 3 | 1 | find_user_id_by_name_zip, get_order_details, modify_user_address | - | - | - | - | - | - | - | 46.66 |
| 41 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | order_id | #W9583042 | #W4082615 | 67 | 72 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
| 42 | 0.0 | ACTION_ONLY | 3 | 3 | modify_pending_order_address, modify_pending_order_address, modify_user_address | - | - | - | - | - | - | - | - |
| 57 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | - | - |
| 59 | 0.0 | ACTION_AND_NL | 2 | 2 | cancel_pending_order, modify_pending_order_address | - | - | - | - | - | - | Agent should tell the user the refund for the cancelled desk lamp order is $1... | 164.28, 625.60 |
| 71 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W5270061', 'address1':... |  | 45 | 0 | MISSING_ACTUAL_CALL | - | - |
| 74 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | payment_method_id | credit_card_4466831 | paypal_5914760 | 17 | 21 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
| 76 | 0.0 | ACTION_ONLY | 1 | 1 | cancel_pending_order | reason | ordered by mistake | no longer needed | 12 | 16 | EXPECTED_AND_ACTUAL_OBSERVED | - | 1939.05 |
| 79 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_items | new_item_ids | ['2439754078'] | ['7661609223'] | 18 | 20 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
| 94 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | item_ids | ['3478699712'] | ['2216662955'] | 9 | 16 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
| 95 | 0.0 | ACTION_AND_NL | 1 | 1 | exchange_delivered_order_items | item_ids | ['3478699712'] | ['2216662955'] | 11 | 18 | EXPECTED_AND_ACTUAL_OBSERVED | Agent should tell the user the price difference for one laptop exchange is $1... | 167.87, 60.78, 107.09 |
| 96 | 0.0 | ACTION_ONLY | 1 | 1 | modify_pending_order_address | $ | {'order_id': '#W6750959', 'address1':... |  | 22 | 0 | MISSING_ACTUAL_CALL | - | - |
| 99 | 0.0 | UNKNOWN | 0 | 0 | - | - | - | - | - | - | - | - | - |
| 98 | 0.0 | ACTION_ONLY | 1 | 1 | exchange_delivered_order_items | new_item_ids | ['5606522780', '6245746168'] | ['5606522780', '5645314103'] | 33 | 36 | EXPECTED_AND_ACTUAL_OBSERVED | - | - |
