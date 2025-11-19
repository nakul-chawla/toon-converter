"""Quick demo of TOON Converter functionality."""

from toon_converter import json_to_toon, toon_to_json, validate_json, validate_toon
import json

print("=" * 60)
print("TOON CONVERTER DEMO")
print("=" * 60)

# Demo 1: Simple Conversion
print("\n1. Simple JSON to TOON Conversion")
print("-" * 60)
data = {
    "name": "Alice Johnson",
    "age": 30,
    "active": True,
    "roles": ["admin", "editor"]
}

print("Original JSON:")
print(json.dumps(data, indent=2))

toon = json_to_toon(data)
print("\nTOON Format:")
print(toon)

print(f"\nToken Reduction: {len(json.dumps(data))} -> {len(toon)} chars")
print(f"Savings: {((len(json.dumps(data)) - len(toon)) / len(json.dumps(data)) * 100):.1f}%")

# Demo 2: Round-trip Conversion
print("\n\n2. Round-trip Conversion (JSON -> TOON -> JSON)")
print("-" * 60)
result = toon_to_json(toon)
print("Converted back to JSON:")
print(json.dumps(result, indent=2))
print(f"[OK] Data preserved: {result == data}")

# Demo 3: Nested Structure
print("\n\n3. Nested Structure")
print("-" * 60)
complex_data = {
    "user": {
        "profile": {
            "name": "Bob",
            "settings": {
                "theme": "dark",
                "notifications": True
            }
        },
        "projects": [
            {"name": "Project A", "status": "active"},
            {"name": "Project B", "status": "completed"}
        ]
    }
}

print("Complex JSON:")
print(json.dumps(complex_data, indent=2))

complex_toon = json_to_toon(complex_data)
print("\nTOON Format:")
print(complex_toon)

print(f"\nToken Reduction: {len(json.dumps(complex_data))} -> {len(complex_toon)} chars")
print(f"Savings: {((len(json.dumps(complex_data)) - len(complex_toon)) / len(json.dumps(complex_data)) * 100):.1f}%")

# Demo 4: Validation
print("\n\n4. Validation")
print("-" * 60)

valid_json = '{"name": "Alice", "age": 30}'
is_valid, error = validate_json(valid_json)
print(f"Valid JSON: {is_valid}")

invalid_json = '{"name": "Alice", "age": }'
is_valid, error = validate_json(invalid_json)
print(f"Invalid JSON: {is_valid}")
print(f"Error: {error}")

valid_toon = "name: Alice\nage: 30"
is_valid, error = validate_toon(valid_toon)
print(f"\nValid TOON: {is_valid}")

invalid_toon = "name: Alice\n age: 30"  # Wrong indentation
is_valid, error = validate_toon(invalid_toon)
print(f"Invalid TOON: {is_valid}")
print(f"Error: {error}")

# Demo 5: Use Case - LLM Prompt
print("\n\n5. Use Case: LLM Prompt Optimization")
print("-" * 60)

config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "features": ["streaming", "functions", "vision"],
    "system": {
        "role": "assistant",
        "context": "helpful AI"
    }
}

json_prompt = f"Configure with: {json.dumps(config)}"
toon_prompt = f"Configure with:\n{json_to_toon(config)}"

print(f"JSON Prompt Length: {len(json_prompt)} chars")
print(f"TOON Prompt Length: {len(toon_prompt)} chars")
print(f"Token Savings: {((len(json_prompt) - len(toon_prompt)) / len(json_prompt) * 100):.1f}%")

print("\n" + "=" * 60)
print("[OK] Demo Complete!")
print("=" * 60)
