"""Test version string handling."""

from toon_converter import json_to_toon, toon_to_json
import json

data = {"version": "2.0"}

print("Original:", data)
print("Type:", type(data["version"]))

toon = json_to_toon(data)
print("\nTOON:", toon)

recovered = toon_to_json(toon)
print("\nRecovered:", recovered)
print("Type:", type(recovered["version"]))

print("\nNote: '2.0' is parsed as float 2.0 (type inference)")
print("This is expected behavior - TOON infers types from values")
print("\nSolution: Use version: v2.0 or version: 2.0.0 to keep as string")

# Test with string-like version
data2 = {"version": "v2.0"}
toon2 = json_to_toon(data2)
recovered2 = toon_to_json(toon2)
print(f"\nWith 'v2.0': {recovered2} (type: {type(recovered2['version'])})")

data3 = {"version": "2.0.0"}
toon3 = json_to_toon(data3)
recovered3 = toon_to_json(toon3)
print(f"With '2.0.0': {recovered3} (type: {type(recovered3['version'])})")
