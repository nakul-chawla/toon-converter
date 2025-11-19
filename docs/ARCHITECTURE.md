# TOON Converter Architecture

## Overview

TOON Converter is a Python library for bidirectional conversion between JSON and TOON (Token-Oriented Object Notation) formats, designed to reduce token usage in LLM prompts by 30-50%.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TOON Converter System                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CLI Tool  │    │  Python API  │    │   REST API   │  │
│  └──────┬──────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                  │                    │          │
│         └──────────────────┼────────────────────┘          │
│                            │                               │
│                   ┌────────▼────────┐                      │
│                   │  Core Library   │                      │
│                   ├─────────────────┤                      │
│                   │  - Converter    │                      │
│                   │  - Parser       │                      │
│                   │  - Validator    │                      │
│                   └────────┬────────┘                      │
│                            │                               │
│                   ┌────────▼────────┐                      │
│                   │  Exceptions     │                      │
│                   └─────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Core Library (`src/toon_converter/core.py`)

**Responsibilities:**
- JSON → TOON conversion
- TOON → JSON parsing
- Recursive structure traversal
- Type preservation

**Key Functions:**
- `json_to_toon(data, indent)`: Convert JSON to TOON
- `toon_to_json(toon_str)`: Parse TOON to JSON
- `_convert_to_toon()`: Recursive converter
- `_parse_toon_lines()`: Line-by-line parser

**Algorithm Flow:**

```
JSON → TOON:
1. Accept dict/list/string input
2. Recursively traverse structure
3. Format based on type:
   - Object: key: value with indentation
   - Array: indented list items
   - Primitives: direct conversion
4. Return formatted string

TOON → JSON:
1. Split into lines
2. Track indentation levels
3. Detect structure type (object/array)
4. Parse values with type inference
5. Reconstruct nested structure
6. Return dict/list
```

### 2. Validator (`src/toon_converter/validator.py`)

**Responsibilities:**
- JSON format validation
- TOON format validation
- Error detail extraction

**Validation Rules:**

**JSON:**
- Valid JSON syntax
- Proper bracket/brace matching
- Correct comma placement

**TOON:**
- Indentation must be multiples of 2
- No indentation jumps > 1 level
- Keys must exist before colons
- Consistent structure

### 3. Exception Handling (`src/toon_converter/exceptions.py`)

**Exception Hierarchy:**
```
TOONError (base)
├── TOONParseError (parsing failures)
├── TOONValidationError (validation failures)
└── JSONValidationError (JSON validation failures)
```

**Error Information:**
- Error message
- Line number (if applicable)
- Column number (if applicable)
- Context information

### 4. CLI Tool (`cli/main.py`)

**Commands:**
- `toon convert <input> [-o output]`: Convert files
- `toon validate <input>`: Validate format

**Features:**
- Auto-detect format by extension
- File I/O handling
- User-friendly error messages

### 5. REST API (`api/app.py`)

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| POST | `/convert/json-to-toon` | Convert JSON to TOON |
| POST | `/convert/toon-to-json` | Convert TOON to JSON |
| POST | `/validate/json` | Validate JSON |
| POST | `/validate/toon` | Validate TOON |
| GET | `/health` | Health check |

**Technology Stack:**
- FastAPI for web framework
- Pydantic for validation
- Uvicorn for ASGI server

## Data Flow

### Conversion Flow

```
┌──────────────────────────────────────────────────────────┐
│ JSON Input                                               │
│ {"user": {"name": "Alice", "age": 30}}                   │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│ json_to_toon()                                           │
│ 1. Parse JSON (if string)                                │
│ 2. Traverse structure recursively                        │
│ 3. Format each level with proper indentation             │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│ TOON Output                                              │
│ user:                                                    │
│   name: Alice                                            │
│   age: 30                                                │
└──────────────────────────────────────────────────────────┘
```

### Parsing Flow

```
┌──────────────────────────────────────────────────────────┐
│ TOON Input                                               │
│ user:                                                    │
│   name: Alice                                            │
│   age: 30                                                │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│ toon_to_json()                                           │
│ 1. Split into lines                                      │
│ 2. Track indentation levels                              │
│ 3. Detect structure (object/array)                       │
│ 4. Parse values with type inference                      │
│ 5. Build nested structure                                │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│ JSON Output                                              │
│ {"user": {"name": "Alice", "age": 30}}                   │
└──────────────────────────────────────────────────────────┘
```

## Type System

| JSON Type | TOON Representation | Parsing Rule |
|-----------|---------------------|--------------|
| Object | `key: value` + indent | Colon with nested indent |
| Array | Indented items | Items at same indent level |
| String | Plain text | Default type |
| Number | Plain number | Regex: `^-?\d+(\.\d+)?$` |
| Boolean | `true` / `false` | Exact match |
| Null | `null` | Exact match |

## Performance Considerations

### Token Reduction

**Example Comparison:**

JSON (87 tokens):
```json
{
  "user": {
    "name": "Alice",
    "roles": ["admin", "editor"]
  }
}
```

TOON (45 tokens):
```
user:
  name: Alice
  roles:
    admin
    editor
```

**Reduction: ~48%**

### Optimization Strategies

1. **Minimal Punctuation**: Remove `{}`, `[]`, `,`, `"`
2. **Whitespace Efficiency**: Use indentation for structure
3. **Type Inference**: No explicit type markers
4. **Compact Arrays**: No separators between items

## Testing Strategy

### Test Coverage

- **Unit Tests**: Individual function testing
- **Integration Tests**: End-to-end conversion
- **Edge Cases**: Special characters, deep nesting, large files
- **Round-trip Tests**: JSON → TOON → JSON consistency

### Test Categories

1. **Conversion Tests**
   - Simple objects
   - Nested structures
   - Arrays
   - Mixed types

2. **Validation Tests**
   - Valid inputs
   - Invalid formats
   - Error reporting

3. **Edge Cases**
   - Unicode characters
   - Special characters in keys/values
   - Empty structures
   - Very deep nesting (100+ levels)
   - Large arrays (1000+ items)

## Deployment

### As Library
```bash
pip install toon-converter
```

### As CLI Tool
```bash
toon convert input.json -o output.toon
```

### As API Service
```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

## Future Enhancements

1. **Streaming Support**: Handle large files without loading into memory
2. **Schema Validation**: Optional schema enforcement
3. **Custom Formatters**: User-defined formatting rules
4. **Compression**: Additional token reduction techniques
5. **Language Bindings**: JavaScript, Go, Rust implementations
