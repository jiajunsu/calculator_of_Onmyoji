# cm\_server API

## / GET

Return index.html
_ _ _

## /calculate POST

### Header
| Key | Value |
|--------|--------|
|Content-Type|application/json|


### Body
| Key | Type | Description |
|--------|--------|--------|
|src_filename|string|filename of source_data, file must be in same dir of cm_server|

For other params, see [Readme](https://github.com/jiajunsu/calculator_of_Onmyoji/blob/master/README.md#usage-of-calculator)

```NOTE: replace '-' to '_' in keys' name```

### Response
| Code | Body_key | Type | Description |
|--------|--------|--------|--------|
| 200 | result_num | int | number of combinations got from calculator |
|  -  | output_file | string | output file path |
| 400 | reason | string | IOError: source_data may not exist or output_file is not writable |
| 500 | reason | string | InternalError: traceback info |

_ _ _
## /status GET

### Response
| Code | Body_key | Type | Description |
|--------|--------|--------|--------|
| 200 | status | string | value is "running" |
|  -  | progress(Optional) | float | calculating precent, between 0 to 1 |
|  -  | current(Optional) | int | calculated combinations |
|  -  | total(Optional) | int | total combinations |
