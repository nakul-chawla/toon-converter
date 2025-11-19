# TOON Converter API Reference

## Python API

### Core Functions

#### `json_to_toon(data, indent=2)`

Convert JSON data to TOON format.

**Parameters:**
- `data` (dict | list | str): JSON data to convert. Can be a dictionary, list, or JSON string.
- `indent` (int, optional): Number of spaces for indentation. Default: 2.

**Returns:**
- `str`: TOON formatted string

**Raises:**
- `json.JSONDecodeError`: If input string is invalid JSON
- `TOONError`: If conversion fails

**Example:**
```python
from toon_converter import json_to_toon

data = {"name": "Alice", "age": 30}
toon = json_to_toon(data)
print(toon)
# Output:
# name: Alice
# age: 30
```

---

#### `toon_to_json(toon_str)`

Convert TOON format to JSON data.

**Parameters:**
- `toon_str` (str): TOON formatted string

**Returns:**
- `dict | list`: Parsed JSON data

**Raises:**
- `TOONParseError`: If TOON parsing fails

**Example:**
```python
from toon_converter import toon_to_json

toon = """name: Alice
age: 30"""
data = toon_to_json(toon)
print(data)
# Output: {'name': 'Alice', 'age': 30}
```

---

#### `validate_json(data)`

Validate JSON string format.

**Parameters:**
- `data` (str): JSON string to validate

**Returns:**
- `tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
from toon_converter import validate_json

is_valid, error = validate_json('{"name": "Alice"}')
if is_valid:
    print("Valid JSON")
else:
    print(f"Invalid: {error}")
```

---

#### `validate_toon(data)`

Validate TOON string format.

**Parameters:**
- `data` (str): TOON string to validate

**Returns:**
- `tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
from toon_converter import validate_toon

is_valid, error = validate_toon("name: Alice\nage: 30")
if is_valid:
    print("Valid TOON")
else:
    print(f"Invalid: {error}")
```

---

#### `get_error_details(error)`

Extract detailed error information from exception.

**Parameters:**
- `error` (Exception): Exception object

**Returns:**
- `dict`: Error details including type, message, line number, column

**Example:**
```python
from toon_converter import toon_to_json, get_error_details, TOONParseError

try:
    data = toon_to_json(invalid_toon)
except TOONParseError as e:
    details = get_error_details(e)
    print(f"Error at line {details.get('line_number')}: {details['message']}")
```

---

### Exception Classes

#### `TOONError`

Base exception for all TOON converter errors.

**Inheritance:** `Exception`

---

#### `TOONParseError`

Raised when TOON parsing fails.

**Inheritance:** `TOONError`

**Attributes:**
- `message` (str): Error message
- `line_number` (int | None): Line number where error occurred
- `column` (int | None): Column number where error occurred

**Example:**
```python
from toon_converter import TOONParseError

try:
    result = toon_to_json(invalid_toon)
except TOONParseError as e:
    print(f"Parse error at line {e.line_number}: {e.message}")
```

---

#### `TOONValidationError`

Raised when TOON validation fails.

**Inheritance:** `TOONError`

---

#### `JSONValidationError`

Raised when JSON validation fails.

**Inheritance:** `TOONError`

---

## REST API

Base URL: `http://localhost:8000`

### Endpoints

#### `GET /`

Get API information and available endpoints.

**Response:**
```json
{
  "name": "TOON Converter API",
  "version": "0.1.0",
  "endpoints": {
    "convert": {
      "json_to_toon": "/convert/json-to-toon",
      "toon_to_json": "/convert/toon-to-json"
    },
    "validate": {
      "json": "/validate/json",
      "toon": "/validate/toon"
    }
  }
}
```

---

#### `POST /convert/json-to-toon`

Convert JSON to TOON format.

**Request Body:**
```json
{
  "data": {"name": "Alice", "age": 30},
  "indent": 2
}
```

**Parameters:**
- `data` (object | array | string): JSON data to convert
- `indent` (integer, optional): Indentation spaces (1-8). Default: 2

**Response:**
```json
{
  "result": "name: Alice\nage: 30",
  "format": "toon"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid input
- `500`: Server error

**Example:**
```bash
curl -X POST http://localhost:8000/convert/json-to-toon \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Alice", "age": 30}, "indent": 2}'
```

---

#### `POST /convert/toon-to-json`

Convert TOON to JSON format.

**Request Body:**
```json
{
  "data": "name: Alice\nage: 30"
}
```

**Parameters:**
- `data` (string): TOON formatted string

**Response:**
```json
{
  "result": "{\n  \"name\": \"Alice\",\n  \"age\": 30\n}",
  "format": "json"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid input
- `500`: Server error

**Example:**
```bash
curl -X POST http://localhost:8000/convert/toon-to-json \
  -H "Content-Type: application/json" \
  -d '{"data": "name: Alice\nage: 30"}'
```

---

#### `POST /validate/json`

Validate JSON format.

**Request Body:**
```json
{
  "data": "{\"name\": \"Alice\"}"
}
```

**Parameters:**
- `data` (string): JSON string to validate

**Response:**
```json
{
  "valid": true,
  "error": "",
  "details": {}
}
```

**Error Response:**
```json
{
  "valid": false,
  "error": "Invalid JSON at line 1, column 15: Expecting value",
  "details": {
    "type": "JSONDecodeError",
    "line_number": 1,
    "column": 15
  }
}
```

**Status Codes:**
- `200`: Success (valid or invalid)
- `500`: Server error

---

#### `POST /validate/toon`

Validate TOON format.

**Request Body:**
```json
{
  "data": "name: Alice\nage: 30"
}
```

**Parameters:**
- `data` (string): TOON string to validate

**Response:**
```json
{
  "valid": true,
  "error": "",
  "details": {}
}
```

**Error Response:**
```json
{
  "valid": false,
  "error": "Line 2: Invalid indentation (must be multiple of 2 spaces)",
  "details": {}
}
```

**Status Codes:**
- `200`: Success (valid or invalid)
- `500`: Server error

---

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200`: Service is healthy

---

## Data Models

### ConvertRequest

Request model for conversion endpoints.

**Fields:**
- `data` (object | array | string): Data to convert
- `indent` (integer, optional): Indentation spaces (1-8). Default: 2

---

### ConvertResponse

Response model for conversion endpoints.

**Fields:**
- `result` (string): Converted data
- `format` (string): Output format ("json" or "toon")

---

### ValidateRequest

Request model for validation endpoints.

**Fields:**
- `data` (string): Data to validate

---

### ValidateResponse

Response model for validation endpoints.

**Fields:**
- `valid` (boolean): Whether data is valid
- `error` (string): Error message if invalid
- `details` (object): Additional error details

---

### ErrorResponse

Error response model.

**Fields:**
- `error` (string): Error message
- `details` (object): Additional error details

---

## Type Mappings

| JSON Type | Python Type | TOON Representation |
|-----------|-------------|---------------------|
| Object | dict | `key: value` with indentation |
| Array | list | Indented list items |
| String | str | Plain text |
| Number | int, float | Plain number |
| Boolean | bool | `true` or `false` |
| Null | None | `null` |

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input data |
| 422 | Validation Error - Request body validation failed |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## Authentication

Currently no authentication is required. For production use, consider adding API key or OAuth authentication.

---

## CORS

CORS is enabled for all origins in development. For production, configure specific allowed origins.

---

## Examples

### Python Client

```python
import requests

# Convert JSON to TOON
response = requests.post(
    "http://localhost:8000/convert/json-to-toon",
    json={"data": {"name": "Alice", "age": 30}}
)
print(response.json()["result"])

# Convert TOON to JSON
response = requests.post(
    "http://localhost:8000/convert/toon-to-json",
    json={"data": "name: Alice\nage: 30"}
)
print(response.json()["result"])
```

### JavaScript Client

```javascript
// Convert JSON to TOON
fetch('http://localhost:8000/convert/json-to-toon', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    data: {name: 'Alice', age: 30}
  })
})
.then(res => res.json())
.then(data => console.log(data.result));
```

### cURL Examples

```bash
# Convert JSON to TOON
curl -X POST http://localhost:8000/convert/json-to-toon \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Alice"}}'

# Validate TOON
curl -X POST http://localhost:8000/validate/toon \
  -H "Content-Type: application/json" \
  -d '{"data": "name: Alice"}'
```
