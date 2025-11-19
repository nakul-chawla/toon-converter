import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath("src"))

from toon_converter import json_to_toon, toon_to_json
import json

def test_ambiguous_type_inference():
    print("\n--- Testing Ambiguous Type Inference ---")
    data = {"zip_code": "01234", "id": "123-456"}
    print(f"Original JSON: {json.dumps(data)}")
    
    toon = json_to_toon(data)
    print(f"TOON Output:\n{toon}")
    
    parsed = toon_to_json(toon)
    print(f"Parsed back: {json.dumps(parsed)}")
    
    if parsed["zip_code"] != "01234":
        print("FAIL: '01234' was parsed as number or modified")
    else:
        print("PASS: '01234' preserved")

def test_keys_with_colons():
    print("\n--- Testing Keys with Colons ---")
    data = {"time:start": "12:00", "normal": "value"}
    print(f"Original JSON: {json.dumps(data)}")
    
    toon = json_to_toon(data)
    print(f"TOON Output:\n{toon}")
    
    try:
        parsed = toon_to_json(toon)
        print(f"Parsed back: {json.dumps(parsed)}")
        if "time:start" in parsed:
            print("PASS: 'time:start' key preserved")
        else:
            print("FAIL: 'time:start' key lost or malformed")
    except Exception as e:
        print(f"FAIL: Parsing error: {e}")

def test_recursion_limit():
    print("\n--- Testing Recursion Limit ---")
    depth = 2000
    data = {"level": "0"}
    current = data
    for i in range(depth):
        current["next"] = {"level": str(i+1)}
        current = current["next"]
    
    try:
        toon = json_to_toon(data)
        # print(f"TOON generated (length: {len(toon)})")
        parsed = toon_to_json(toon)
        print("PASS: Deep recursion handled")
    except RecursionError:
        print("FAIL: RecursionError hit")
    except Exception as e:
        print(f"FAIL: Other error: {e}")

if __name__ == "__main__":
    test_ambiguous_type_inference()
    test_keys_with_colons()
    test_recursion_limit()
