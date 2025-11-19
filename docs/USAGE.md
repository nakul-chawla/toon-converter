# TOON Converter Usage Guide

## Installation

```bash
pip install toon-converter
```

For development:
```bash
pip install toon-converter[dev]
```

For API support:
```bash
pip install toon-converter[api]
```

## Python Library Usage

### Basic Conversion

```python
from toon_converter import json_to_toon, toon_to_json

# JSON to TOON
data = {
    "name": "Alice",
    "age": 30,
    "roles": ["admin", "editor"]
}

toon = json_to_toon(data)
print(toon)
# Output:
# name: Alice
# age: 30
# roles:
#   admin
#   editor

# TOON to JSON
json_data = toon_to_json(toon)
print(json_data)
# Output: {'name': 'Alice', 'age': 30, 'roles': ['admin', 'editor']}
```

### Custom Indentation

```python
# Use 4 spaces instead of 2
toon = json_to_toon(data, indent=4)
```

### Validation

```python
from toon_converter import validate_json, validate_toon

# Validate JSON
is_valid, error = validate_json('{"name": "Alice"}')
if not is_valid:
    print(f"Error: {error}")

# Validate TOON
is_valid, error = validate_toon("name: Alice\nage: 30")
if not is_valid:
    print(f"Error: {error}")
```

### Error Handling

```python
from toon_converter import json_to_toon, TOONParseError, get_error_details

try:
    result = toon_to_json(invalid_toon)
except TOONParseError as e:
    details = get_error_details(e)
    print(f"Parse error at line {details['line_number']}: {details['message']}")
```

## CLI Usage

### Convert Files

```bash
# JSON to TOON
toon convert input.json -o output.toon

# TOON to JSON
toon convert input.toon -o output.json

# Auto-detect output filename
toon convert input.json  # Creates input.toon
```

### Validate Files

```bash
# Validate JSON
toon validate data.json

# Validate TOON
toon validate data.toon
```

### Examples

```bash
# Convert example file
cd examples
toon convert sample.json -o sample_output.toon

# Validate example
toon validate sample.toon
```

## API Usage

### Start Server

```bash
# Development
uvicorn api.app:app --reload

# Production
uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Endpoints

#### Convert JSON to TOON

```bash
curl -X POST http://localhost:8000/convert/json-to-toon \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"name": "Alice", "age": 30},
    "indent": 2
  }'
```

Response:
```json
{
  "result": "name: Alice\nage: 30",
  "format": "toon"
}
```

#### Convert TOON to JSON

```bash
curl -X POST http://localhost:8000/convert/toon-to-json \
  -H "Content-Type: application/json" \
  -d '{
    "data": "name: Alice\nage: 30"
  }'
```

Response:
```json
{
  "result": "{\n  \"name\": \"Alice\",\n  \"age\": 30\n}",
  "format": "json"
}
```

#### Validate JSON

```bash
curl -X POST http://localhost:8000/validate/json \
  -H "Content-Type: application/json" \
  -d '{
    "data": "{\"name\": \"Alice\"}"
  }'
```

Response:
```json
{
  "valid": true,
  "error": "",
  "details": {}
}
```

#### Validate TOON

```bash
curl -X POST http://localhost:8000/validate/toon \
  -H "Content-Type: application/json" \
  -d '{
    "data": "name: Alice\nage: 30"
  }'
```

Response:
```json
{
  "valid": true,
  "error": "",
  "details": {}
}
```

#### Health Check

```bash
curl http://localhost:8000/health
```

## Advanced Usage

### Working with Files

```python
import json
from pathlib import Path
from toon_converter import json_to_toon, toon_to_json

# Read JSON file and convert to TOON
json_file = Path("data.json")
data = json.loads(json_file.read_text())
toon = json_to_toon(data)
Path("data.toon").write_text(toon)

# Read TOON file and convert to JSON
toon_file = Path("data.toon")
toon_content = toon_file.read_text()
data = toon_to_json(toon_content)
Path("data.json").write_text(json.dumps(data, indent=2))
```

### Batch Processing

```python
from pathlib import Path
from toon_converter import json_to_toon

# Convert all JSON files in directory
for json_file in Path("data").glob("*.json"):
    data = json.loads(json_file.read_text())
    toon = json_to_toon(data)
    output_file = json_file.with_suffix(".toon")
    output_file.write_text(toon)
    print(f"Converted {json_file} -> {output_file}")
```

### Integration with LLM Prompts

```python
from toon_converter import json_to_toon

# Prepare data for LLM prompt
config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "features": ["streaming", "functions"]
}

# Convert to TOON for token efficiency
toon_config = json_to_toon(config)

prompt = f"""
Configure the model with these settings:

{toon_config}

Generate a response based on this configuration.
"""

# This uses ~30% fewer tokens than including raw JSON
```

## Best Practices

### 1. Use TOON for LLM Prompts

TOON is ideal for including configuration or data in prompts:
- ✅ Reduces token usage by 30-50%
- ✅ More readable than compact JSON
- ✅ Preserves structure and types

### 2. Keep JSON for APIs

Use standard JSON for API communication:
- ✅ Universal compatibility
- ✅ Built-in validation
- ✅ Tool support

### 3. Validate Before Converting

Always validate input before conversion:
```python
is_valid, error = validate_json(json_string)
if is_valid:
    toon = json_to_toon(json_string)
```

### 4. Handle Errors Gracefully

```python
try:
    result = toon_to_json(toon_string)
except TOONParseError as e:
    # Log error with details
    logger.error(f"TOON parse error: {e}")
    # Fallback to default
    result = {}
```

### 5. Use Appropriate Indentation

- 2 spaces: Default, most compact
- 4 spaces: Better readability for complex structures

## Common Patterns

### Configuration Files

```python
# config.toon
server:
  host: localhost
  port: 8000
  workers: 4
database:
  url: postgresql://localhost/db
  pool_size: 10
features:
  auth
  logging
  metrics
```

### API Responses

```python
# Convert API response to TOON for logging
response = api.get_user(user_id)
toon_log = json_to_toon(response)
logger.info(f"User data:\n{toon_log}")
```

### Data Serialization

```python
# Serialize complex objects
class User:
    def to_toon(self):
        data = {
            "id": self.id,
            "name": self.name,
            "profile": self.profile.__dict__
        }
        return json_to_toon(data)
```

## Troubleshooting

### Issue: Indentation errors

**Problem**: TOON validation fails with indentation error

**Solution**: Ensure indentation is multiples of 2 spaces
```python
# Wrong (1 space)
user:
 name: Alice

# Correct (2 spaces)
user:
  name: Alice
```

### Issue: Type conversion

**Problem**: Numbers parsed as strings

**Solution**: TOON infers types automatically. Ensure values match expected format:
```python
# Will be parsed as number
age: 30

# Will be parsed as string
age: 30years
```

### Issue: Special characters

**Problem**: Colons in values cause parsing errors

**Solution**: Colons in values are preserved after the first colon:
```python
# Correct - everything after first colon is the value
time: 12:30:45
url: http://example.com
```

## Performance Tips

1. **Large Files**: Process in chunks if memory is limited
2. **Batch Operations**: Convert multiple files in parallel
3. **Caching**: Cache converted results for repeated use
4. **Validation**: Skip validation for trusted sources

## Next Steps

- Read [Architecture Documentation](ARCHITECTURE.md)
- Explore [API Reference](API.md)
- Check [Examples](../examples/)
- Contribute on [GitHub](https://github.com/yourusername/toon-converter)
