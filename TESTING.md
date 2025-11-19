# TOON Converter - Testing Guide

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=toon_converter --cov-report=html

# Run specific test file
pytest tests/test_json_to_toon.py

# Run specific test
pytest tests/test_json_to_toon.py::test_simple_object
```

## Test Structure

```
tests/
├── __init__.py
├── test_json_to_toon.py      # JSON → TOON conversion (15 tests)
├── test_toon_to_json.py      # TOON → JSON parsing (17 tests)
├── test_validator.py         # Validation functions (12 tests)
├── test_edge_cases.py        # Edge cases & round-trips (20 tests)
└── fixtures/                 # Test data files
```

## Test Categories

### 1. JSON to TOON Conversion (15 tests)

**Coverage:**
- Simple objects
- Nested objects
- Arrays (simple, numeric, mixed)
- Mixed data types
- Empty structures
- Deep nesting
- Special characters
- Custom indentation
- Boolean values
- Array of objects

**Run:**
```bash
pytest tests/test_json_to_toon.py -v
```

### 2. TOON to JSON Parsing (17 tests)

**Coverage:**
- Simple object parsing
- Nested object parsing
- Array parsing
- Type inference (string, number, boolean, null)
- Empty values
- Deep nesting
- Special characters
- Whitespace handling
- Float numbers
- Negative numbers

**Run:**
```bash
pytest tests/test_toon_to_json.py -v
```

### 3. Validation (12 tests)

**Coverage:**
- Valid JSON validation
- Invalid JSON detection
- Valid TOON validation
- Invalid TOON detection
- Indentation validation
- Empty key detection
- Error detail extraction
- Complex structure validation

**Run:**
```bash
pytest tests/test_validator.py -v
```

### 4. Edge Cases (20 tests)

**Coverage:**
- Round-trip conversions (JSON → TOON → JSON)
- Unicode characters
- Special keys
- Numeric strings
- Empty strings
- Very deep nesting (10+ levels)
- Large arrays (100+ items)
- Mixed nested structures
- Zero and false values
- Negative numbers
- Scientific notation
- Whitespace in values
- Colons in values

**Run:**
```bash
pytest tests/test_edge_cases.py -v
```

## Manual Testing

### CLI Testing

```bash
# Test conversion
cd examples
python -m cli.main convert sample.json -o output.toon
python -m cli.main convert output.toon -o output.json

# Test validation
python -m cli.main validate sample.json
python -m cli.main validate sample.toon

# Test error handling
python -m cli.main convert nonexistent.json
```

### API Testing

```bash
# Start server
uvicorn api.app:app --reload

# Test in another terminal
curl http://localhost:8000/

# Test conversion
curl -X POST http://localhost:8000/convert/json-to-toon \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Alice", "age": 30}}'

# Test validation
curl -X POST http://localhost:8000/validate/json \
  -H "Content-Type: application/json" \
  -d '{"data": "{\"name\": \"Alice\"}"}'

# Test health
curl http://localhost:8000/health
```

### Python Library Testing

```python
# Create test script: test_manual.py
from toon_converter import json_to_toon, toon_to_json

# Test 1: Simple conversion
data = {"name": "Alice", "age": 30}
toon = json_to_toon(data)
print("TOON:", toon)
result = toon_to_json(toon)
print("JSON:", result)
assert result == data, "Round-trip failed!"

# Test 2: Complex structure
data = {
    "user": {
        "profile": {
            "settings": {
                "theme": "dark"
            }
        }
    }
}
toon = json_to_toon(data)
result = toon_to_json(toon)
assert result == data, "Complex round-trip failed!"

print("✓ All manual tests passed!")
```

Run:
```bash
python test_manual.py
```

## Performance Testing

### Token Reduction Test

```python
# Create test script: test_performance.py
import json
from toon_converter import json_to_toon

data = {
    "user": {
        "name": "Alice",
        "age": 30,
        "roles": ["admin", "editor", "viewer"],
        "profile": {
            "bio": "Software engineer",
            "settings": {
                "theme": "dark",
                "notifications": True
            }
        }
    }
}

json_str = json.dumps(data)
toon_str = json_to_toon(data)

json_tokens = len(json_str)
toon_tokens = len(toon_str)
reduction = ((json_tokens - toon_tokens) / json_tokens) * 100

print(f"JSON size: {json_tokens} chars")
print(f"TOON size: {toon_tokens} chars")
print(f"Reduction: {reduction:.1f}%")
```

### Large Data Test

```python
# Create test script: test_large.py
from toon_converter import json_to_toon, toon_to_json
import time

# Generate large dataset
data = {
    "items": [
        {"id": i, "name": f"Item {i}", "value": i * 10}
        for i in range(1000)
    ]
}

# Test conversion speed
start = time.time()
toon = json_to_toon(data)
json_to_toon_time = time.time() - start

start = time.time()
result = toon_to_json(toon)
toon_to_json_time = time.time() - start

print(f"JSON → TOON: {json_to_toon_time:.3f}s")
print(f"TOON → JSON: {toon_to_json_time:.3f}s")
print(f"Items: {len(result['items'])}")
```

## Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=toon_converter --cov-report=html

# Open report
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

## Code Quality Checks

### Format Code

```bash
# Check formatting
black --check src/ tests/

# Apply formatting
black src/ tests/
```

### Lint Code

```bash
# Run flake8
flake8 src/ tests/ --max-line-length=100
```

### Type Checking

```bash
# Run mypy
mypy src/toon_converter/
```

## Continuous Testing

### Watch Mode

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Test Results

Expected output:
```
======================== test session starts ========================
collected 64 items

tests/test_json_to_toon.py ............... [ 23%]
tests/test_toon_to_json.py ................. [ 50%]
tests/test_validator.py ............ [ 68%]
tests/test_edge_cases.py .................... [100%]

======================== 64 passed in 0.50s =========================
```

## Troubleshooting

### Import Errors

```bash
# Install in development mode
pip install -e .
```

### Missing Dependencies

```bash
# Install all dev dependencies
pip install -e ".[dev,api]"
```

### Test Failures

1. Check Python version (requires 3.8+)
2. Verify all dependencies installed
3. Check for file path issues (Windows vs Unix)
4. Review error messages carefully

## Next Steps

1. ✅ Run all tests: `pytest`
2. ✅ Check coverage: `pytest --cov`
3. ✅ Format code: `black src/ tests/`
4. ✅ Lint code: `flake8 src/ tests/`
5. ✅ Manual CLI testing
6. ✅ Manual API testing
7. ✅ Performance testing
8. ✅ Review coverage report

## Success Criteria

- [ ] All 64 tests pass
- [ ] Coverage > 70%
- [ ] No linting errors
- [ ] CLI works correctly
- [ ] API works correctly
- [ ] Performance acceptable
- [ ] Documentation complete
