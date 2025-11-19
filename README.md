# TOON Converter

**Token-Oriented Object Notation** - A compact, human-readable format for serializing JSON data in LLM prompts.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Features

- ✅ Bidirectional JSON ↔ TOON conversion
- ✅ 30-50% token reduction vs standard JSON
- ✅ Multi-level nested structure support
- ✅ Comprehensive validation & error reporting
- ✅ CLI tool for file processing
- ✅ REST API for integration
- ✅ Production-ready library

## 📦 Installation

```bash
pip install toon-converter
```

## 🚀 Quick Start

### Python Library

```python
from toon_converter import json_to_toon, toon_to_json

# JSON to TOON
data = {"name": "Alice", "age": 30, "roles": ["admin", "editor"]}
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
```

### CLI Usage

```bash
# Convert JSON to TOON
toon convert input.json -o output.toon

# Convert TOON to JSON
toon convert input.toon -o output.json

# Validate files
toon validate input.toon
```

### API Usage

```bash
# Start server
uvicorn api.app:app --reload

# Convert via API
curl -X POST http://localhost:8000/convert/json-to-toon \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 30}'
```

## 📖 Format Specification

### TOON Format Rules

1. **Objects**: Key-value pairs with `:` separator
2. **Arrays**: Indented list items (no brackets)
3. **Nesting**: Indentation-based structure
4. **Types**: Automatic inference (string, number, boolean, null)

### Examples

**Simple Object**
```
name: Alice
age: 30
active: true
```

**Nested Structure**
```
user:
  profile:
    name: Alice
    settings:
      theme: dark
      notifications: true
```

**Arrays**
```
items:
  apple
  banana
  orange
numbers:
  1
  2
  3
```

**Mixed Types**
```
config:
  name: MyApp
  version: 1.0
  enabled: true
  maxRetries: 3
  timeout: null
  features:
    auth
    logging
```

## 🏗️ Project Structure

```
toon-converter/
├── src/toon_converter/    # Core library
├── tests/                 # Test suite
├── cli/                   # CLI tool
├── api/                   # REST API
├── docs/                  # Documentation
└── examples/              # Usage examples
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=toon_converter --cov-report=html

# Run specific test
pytest tests/test_json_to_toon.py
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Usage Guide](docs/USAGE.md)

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines.

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Links

- GitHub: https://github.com/yourusername/toon-converter
- PyPI: https://pypi.org/project/toon-converter/
