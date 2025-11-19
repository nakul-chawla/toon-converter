# TOON Converter - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Installation

```bash
cd toon-converter
pip install -e .
```

### Step 2: Run Tests

```bash
pytest
```

Expected output: `60 passed in 0.47s` ✓

### Step 3: Try the Demo

```bash
python demo.py
```

You'll see:
- JSON to TOON conversion
- Round-trip conversion
- Nested structures
- Validation examples
- Token savings metrics

### Step 4: Use the Library

Create `test.py`:

```python
from toon_converter import json_to_toon, toon_to_json

# Your data
data = {
    "name": "Alice",
    "age": 30,
    "roles": ["admin", "editor"]
}

# Convert to TOON
toon = json_to_toon(data)
print(toon)

# Convert back to JSON
result = toon_to_json(toon)
print(result)
```

Run it:
```bash
python test.py
```

### Step 5: Try the CLI

```bash
# Convert JSON to TOON
python -m cli.main convert examples/sample.json -o output.toon

# Convert TOON to JSON
python -m cli.main convert output.toon -o output.json

# Validate
python -m cli.main validate examples/sample.json
```

### Step 6: Start the API (Optional)

```bash
# Install API dependencies
pip install fastapi uvicorn pydantic

# Start server
uvicorn api.app:app --reload
```

Visit: http://localhost:8000

Test with curl:
```bash
curl -X POST http://localhost:8000/convert/json-to-toon \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Alice", "age": 30}}'
```

---

## 📖 Common Use Cases

### 1. Reduce LLM Prompt Tokens

```python
from toon_converter import json_to_toon

config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "features": ["streaming", "functions"]
}

# Use in prompt
prompt = f"""
Configure the model:
{json_to_toon(config)}

Generate a response.
"""
# Saves 15-35% tokens!
```

### 2. Readable Config Files

```python
# config.toon
server:
  host: localhost
  port: 8000
database:
  url: postgresql://localhost/db
  pool_size: 10
```

Load it:
```python
from pathlib import Path
from toon_converter import toon_to_json

config = toon_to_json(Path("config.toon").read_text())
```

### 3. Data Validation

```python
from toon_converter import validate_json, validate_toon

# Validate before processing
is_valid, error = validate_json(user_input)
if not is_valid:
    print(f"Error: {error}")
```

---

## 🎯 Key Functions

### Convert JSON to TOON
```python
json_to_toon(data, indent=2)
```

### Convert TOON to JSON
```python
toon_to_json(toon_string)
```

### Validate JSON
```python
validate_json(json_string)  # Returns (bool, error_msg)
```

### Validate TOON
```python
validate_toon(toon_string)  # Returns (bool, error_msg)
```

---

## 📚 Learn More

- **Full Documentation**: See `docs/USAGE.md`
- **API Reference**: See `docs/API.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Examples**: Check `examples/` directory

---

## ✅ Verification Checklist

- [ ] Tests pass: `pytest`
- [ ] Demo runs: `python demo.py`
- [ ] CLI works: `python -m cli.main --help`
- [ ] Library imports: `from toon_converter import json_to_toon`
- [ ] API starts: `uvicorn api.app:app`

---

## 🆘 Troubleshooting

### Import Error
```bash
pip install -e .
```

### Tests Fail
```bash
pip install pytest pytest-cov
```

### API Won't Start
```bash
pip install fastapi uvicorn pydantic
```

---

## 🎉 You're Ready!

Start converting JSON to TOON and save tokens in your LLM prompts!

**Next Steps:**
1. Read full documentation
2. Try with your own data
3. Integrate into your project
4. Share with others!
