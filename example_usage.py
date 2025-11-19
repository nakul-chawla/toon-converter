"""Simple example of using TOON Converter as a library."""

from toon_converter import json_to_toon, toon_to_json

# Example 1: Basic conversion
print("Example 1: Basic Conversion")
print("-" * 40)

user_data = {
    "name": "John Doe",
    "age": 28,
    "email": "john@example.com"
}

# Convert to TOON
toon_output = json_to_toon(user_data)
print("TOON format:")
print(toon_output)

# Convert back to JSON
json_output = toon_to_json(toon_output)
print("\nBack to JSON:", json_output)


# Example 2: Use in LLM prompt (save tokens!)
print("\n\nExample 2: LLM Prompt Optimization")
print("-" * 40)

api_config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 500,
    "features": ["streaming", "json_mode"]
}

# Instead of sending JSON in prompt
prompt_with_toon = f"""
Please configure the API with these settings:

{json_to_toon(api_config)}

Generate a response based on this configuration.
"""

print(prompt_with_toon)
print(f"Token savings: ~30% compared to JSON!")


# Example 3: Read/Write files
print("\n\nExample 3: File Operations")
print("-" * 40)

from pathlib import Path

# Save as TOON file
config = {"database": {"host": "localhost", "port": 5432}}
Path("config.toon").write_text(json_to_toon(config))
print("Saved config.toon")

# Load from TOON file
loaded_config = toon_to_json(Path("config.toon").read_text())
print("Loaded config:", loaded_config)


# Example 4: Validation
print("\n\nExample 4: Validation")
print("-" * 40)

from toon_converter import validate_toon

toon_data = """name: Alice
age: 30
active: true"""

is_valid, error = validate_toon(toon_data)
if is_valid:
    print("[OK] Valid TOON format")
    data = toon_to_json(toon_data)
    print("Parsed data:", data)
else:
    print(f"[ERROR] Invalid: {error}")
