"""Test array of objects fix."""

from toon_converter import json_to_toon, toon_to_json
import json

print("=" * 70)
print("ARRAY OF OBJECTS - FIX TEST")
print("=" * 70)

# Test 1: Simple array of objects
print("\n1. Simple Array of Objects")
print("-" * 70)

data = {
    "users": [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]
}

print("Original JSON:")
print(json.dumps(data, indent=2))

toon = json_to_toon(data)
print("\nTOON Format:")
print(toon)

recovered = toon_to_json(toon)
print("\nRecovered JSON:")
print(json.dumps(recovered, indent=2))

matches = (
    len(recovered["users"]) == 3 and
    recovered["users"][0]["name"] == "Alice" and
    recovered["users"][1]["name"] == "Bob" and
    recovered["users"][2]["name"] == "Charlie"
)
print(f"\n[{'OK' if matches else 'FAIL'}] Test 1: {matches}")


# Test 2: Nested array of objects
print("\n\n2. Nested Array of Objects")
print("-" * 70)

data = {
    "projects": [
        {
            "name": "Project A",
            "status": "active",
            "team": {
                "lead": "Alice",
                "size": 5
            }
        },
        {
            "name": "Project B",
            "status": "completed",
            "team": {
                "lead": "Bob",
                "size": 3
            }
        }
    ]
}

print("Original JSON:")
print(json.dumps(data, indent=2))

toon = json_to_toon(data)
print("\nTOON Format:")
print(toon)

recovered = toon_to_json(toon)
print("\nRecovered JSON:")
print(json.dumps(recovered, indent=2))

matches = (
    len(recovered["projects"]) == 2 and
    recovered["projects"][0]["name"] == "Project A" and
    recovered["projects"][0]["team"]["lead"] == "Alice" and
    recovered["projects"][1]["name"] == "Project B"
)
print(f"\n[{'OK' if matches else 'FAIL'}] Test 2: {matches}")


# Test 3: Mixed array (simple values and objects)
print("\n\n3. Simple Array (strings)")
print("-" * 70)

data = {
    "tags": ["python", "javascript", "rust"]
}

print("Original JSON:")
print(json.dumps(data, indent=2))

toon = json_to_toon(data)
print("\nTOON Format:")
print(toon)

recovered = toon_to_json(toon)
print("\nRecovered JSON:")
print(json.dumps(recovered, indent=2))

matches = (
    recovered["tags"] == ["python", "javascript", "rust"]
)
print(f"\n[{'OK' if matches else 'FAIL'}] Test 3: {matches}")


# Test 4: Large array of objects
print("\n\n4. Large Array (100 objects)")
print("-" * 70)

data = {
    "items": [
        {"id": i, "name": f"Item {i}", "value": i * 10}
        for i in range(100)
    ]
}

toon = json_to_toon(data)
recovered = toon_to_json(toon)

matches = (
    len(recovered["items"]) == 100 and
    recovered["items"][0]["id"] == 0 and
    recovered["items"][99]["id"] == 99 and
    recovered["items"][50]["value"] == 500
)
print(f"[{'OK' if matches else 'FAIL'}] Large array: {matches}")
print(f"Items count: {len(recovered['items'])}")
print(f"First item: {recovered['items'][0]}")
print(f"Last item: {recovered['items'][99]}")


print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("Array of objects now properly supported with '-' marker!")
print("=" * 70)
