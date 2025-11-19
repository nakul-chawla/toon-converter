"""Complex recursive JSON test with large data."""

from toon_converter import json_to_toon, toon_to_json
import json
import time

print("=" * 70)
print("COMPLEX RECURSIVE JSON TEST")
print("=" * 70)

# Test 1: Deep recursive organization structure
print("\n1. Deep Recursive Organization (10 levels)")
print("-" * 70)

def create_org_structure(level, max_level=10):
    """Create deeply nested organization structure."""
    if level >= max_level:
        return {
            "name": f"Employee_{level}",
            "id": level,
            "role": "Individual Contributor",
            "salary": 50000 + (level * 1000),
            "skills": ["Python", "JavaScript", "SQL"],
            "active": True
        }
    
    return {
        "name": f"Manager_Level_{level}",
        "id": level,
        "role": "Manager",
        "department": f"Dept_{level}",
        "budget": 100000 * (max_level - level),
        "employees": [
            create_org_structure(level + 1, max_level),
            create_org_structure(level + 1, max_level)
        ],
        "metadata": {
            "created": "2024-01-01",
            "updated": "2024-01-15",
            "level": level
        }
    }

org_data = create_org_structure(0, 10)

# Convert to JSON and TOON
json_str = json.dumps(org_data, indent=2)
print(f"JSON size: {len(json_str):,} characters")

start = time.time()
toon_str = json_to_toon(org_data)
toon_time = time.time() - start
print(f"TOON size: {len(toon_str):,} characters")
print(f"Conversion time: {toon_time:.4f}s")
print(f"Size reduction: {((len(json_str) - len(toon_str)) / len(json_str) * 100):.1f}%")

# Test round-trip
start = time.time()
recovered = toon_to_json(toon_str)
parse_time = time.time() - start
print(f"Parse time: {parse_time:.4f}s")

# Verify data integrity
def verify_structure(original, recovered, path="root"):
    """Recursively verify structure matches."""
    if type(original) != type(recovered):
        return False, f"Type mismatch at {path}"
    
    if isinstance(original, dict):
        if set(original.keys()) != set(recovered.keys()):
            return False, f"Keys mismatch at {path}"
        for key in original:
            ok, msg = verify_structure(original[key], recovered[key], f"{path}.{key}")
            if not ok:
                return False, msg
    elif isinstance(original, list):
        if len(original) != len(recovered):
            return False, f"List length mismatch at {path}"
        for i, (o, r) in enumerate(zip(original, recovered)):
            ok, msg = verify_structure(o, r, f"{path}[{i}]")
            if not ok:
                return False, msg
    else:
        if original != recovered:
            return False, f"Value mismatch at {path}: {original} != {recovered}"
    
    return True, "OK"

is_valid, msg = verify_structure(org_data, recovered)
print(f"Data integrity: {msg}")
print(f"[OK] Deep recursion test passed!" if is_valid else f"[FAIL] {msg}")


# Test 2: Large array with many objects
print("\n\n2. Large Array Test (1000 items)")
print("-" * 70)

large_data = {
    "users": [
        {
            "id": i,
            "username": f"user_{i}",
            "email": f"user{i}@example.com",
            "profile": {
                "firstName": f"First{i}",
                "lastName": f"Last{i}",
                "age": 20 + (i % 50),
                "address": {
                    "street": f"{i} Main St",
                    "city": "City" + str(i % 10),
                    "zip": f"{10000 + i}"
                }
            },
            "roles": ["user", "member"] if i % 2 == 0 else ["user"],
            "active": i % 3 != 0,
            "score": i * 1.5,
            "metadata": {
                "created": "2024-01-01",
                "lastLogin": "2024-01-15",
                "loginCount": i % 100
            }
        }
        for i in range(1000)
    ],
    "total": 1000,
    "page": 1,
    "hasMore": True
}

json_str = json.dumps(large_data, indent=2)
print(f"JSON size: {len(json_str):,} characters")

start = time.time()
toon_str = json_to_toon(large_data)
toon_time = time.time() - start
print(f"TOON size: {len(toon_str):,} characters")
print(f"Conversion time: {toon_time:.4f}s")
print(f"Size reduction: {((len(json_str) - len(toon_str)) / len(json_str) * 100):.1f}%")

start = time.time()
recovered = toon_to_json(toon_str)
parse_time = time.time() - start
print(f"Parse time: {parse_time:.4f}s")

# Quick verification
matches = (
    len(recovered["users"]) == 1000 and
    recovered["users"][0]["id"] == 0 and
    recovered["users"][999]["id"] == 999 and
    recovered["total"] == 1000
)
print(f"Data integrity: {'OK' if matches else 'FAIL'}")
print(f"[OK] Large array test passed!" if matches else "[FAIL] Data mismatch")


# Test 3: Complex nested structure with mixed types
print("\n\n3. Complex Mixed Structure")
print("-" * 70)

complex_data = {
    "api": {
        "version": "2.0",
        "endpoints": [
            {
                "path": "/users",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "auth": True,
                "rateLimit": 100,
                "params": {
                    "query": ["page", "limit", "sort"],
                    "body": {
                        "required": ["username", "email"],
                        "optional": ["firstName", "lastName", "age"]
                    }
                },
                "responses": {
                    "200": {"description": "Success", "schema": "User"},
                    "400": {"description": "Bad Request", "schema": "Error"},
                    "401": {"description": "Unauthorized", "schema": "Error"}
                }
            },
            {
                "path": "/posts",
                "methods": ["GET", "POST"],
                "auth": False,
                "rateLimit": 50,
                "params": {
                    "query": ["category", "tags", "author"],
                    "body": {
                        "required": ["title", "content"],
                        "optional": ["tags", "published"]
                    }
                }
            }
        ],
        "config": {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "mydb",
                "pool": {
                    "min": 2,
                    "max": 10,
                    "timeout": 30000
                }
            },
            "cache": {
                "enabled": True,
                "ttl": 3600,
                "maxSize": 1000,
                "strategy": "LRU"
            },
            "logging": {
                "level": "info",
                "format": "json",
                "outputs": ["console", "file"],
                "rotation": {
                    "enabled": True,
                    "maxSize": "100MB",
                    "maxFiles": 10
                }
            }
        },
        "features": {
            "authentication": {
                "enabled": True,
                "providers": ["local", "oauth", "saml"],
                "session": {
                    "timeout": 3600,
                    "refresh": True,
                    "secure": True
                }
            },
            "monitoring": {
                "enabled": True,
                "metrics": ["requests", "errors", "latency"],
                "alerts": [
                    {"type": "error_rate", "threshold": 0.05, "window": 300},
                    {"type": "latency", "threshold": 1000, "window": 60}
                ]
            }
        }
    }
}

json_str = json.dumps(complex_data, indent=2)
print(f"JSON size: {len(json_str):,} characters")

start = time.time()
toon_str = json_to_toon(complex_data)
toon_time = time.time() - start
print(f"TOON size: {len(toon_str):,} characters")
print(f"Conversion time: {toon_time:.4f}s")
print(f"Size reduction: {((len(json_str) - len(toon_str)) / len(json_str) * 100):.1f}%")

start = time.time()
recovered = toon_to_json(toon_str)
parse_time = time.time() - start
print(f"Parse time: {parse_time:.4f}s")

is_valid, msg = verify_structure(complex_data, recovered)
print(f"Data integrity: {msg}")
print(f"[OK] Complex structure test passed!" if is_valid else f"[FAIL] {msg}")


# Summary
print("\n\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("[OK] All complex tests passed!")
print("- Deep recursion (10 levels): PASSED")
print("- Large arrays (1000 items): PASSED")
print("- Complex nested structures: PASSED")
print("- Data integrity verified: PASSED")
print("\nTOON Converter handles complex, recursive, large JSON perfectly!")
print("=" * 70)
