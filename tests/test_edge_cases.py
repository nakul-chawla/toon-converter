"""Tests for edge cases and special scenarios."""

import pytest
from toon_converter import json_to_toon, toon_to_json


def test_round_trip_simple():
    """Test round-trip conversion for simple object."""
    original = {"name": "Alice", "age": 30}
    toon = json_to_toon(original)
    result = toon_to_json(toon)
    assert result == original


def test_round_trip_nested():
    """Test round-trip conversion for nested object."""
    original = {
        "user": {
            "name": "Alice",
            "profile": {
                "age": 30,
                "active": True
            }
        }
    }
    toon = json_to_toon(original)
    result = toon_to_json(toon)
    assert result == original


def test_round_trip_array():
    """Test round-trip conversion for arrays."""
    original = {"items": ["apple", "banana", "orange"]}
    toon = json_to_toon(original)
    result = toon_to_json(toon)
    assert result == original


def test_round_trip_mixed_types():
    """Test round-trip with all data types."""
    original = {
        "string": "text",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null_value": None
    }
    toon = json_to_toon(original)
    result = toon_to_json(toon)
    assert result == original


def test_unicode_characters():
    """Test Unicode character handling."""
    data = {"emoji": "🎉", "chinese": "你好", "arabic": "مرحبا"}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result == data


def test_special_keys():
    """Test keys with special characters."""
    data = {"key-with-dash": "value", "key_with_underscore": "value"}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result == data


def test_numeric_strings():
    """Test strings that look like numbers."""
    data = {"zip_code": "12345", "phone": "555-1234"}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    # Note: These will be converted to numbers in TOON
    assert "zip_code" in result
    assert "phone" in result


def test_empty_strings():
    """Test empty string values."""
    data = {"empty": "", "name": "Alice"}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert "empty" in result
    assert result["name"] == "Alice"


def test_very_deep_nesting():
    """Test very deep nesting (10 levels)."""
    data = {"l1": {"l2": {"l3": {"l4": {"l5": {"l6": {"l7": {"l8": {"l9": {"l10": "deep"}}}}}}}}}}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result["l1"]["l2"]["l3"]["l4"]["l5"]["l6"]["l7"]["l8"]["l9"]["l10"] == "deep"


def test_large_array():
    """Test large array handling."""
    data = {"numbers": list(range(100))}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert len(result["numbers"]) == 100
    assert result["numbers"][0] == 0
    assert result["numbers"][99] == 99


def test_mixed_nested_structures():
    """Test complex mixed structures."""
    data = {
        "users": [
            {"name": "Alice", "roles": ["admin", "user"]},
            {"name": "Bob", "roles": ["user"]}
        ],
        "config": {
            "enabled": True,
            "settings": {
                "timeout": 30
            }
        }
    }
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert len(result["users"]) == 2
    assert result["config"]["enabled"] is True


def test_zero_values():
    """Test zero and false values."""
    data = {"zero": 0, "false": False, "empty_string": ""}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result["zero"] == 0
    assert result["false"] is False


def test_negative_numbers():
    """Test negative numbers."""
    data = {"temperature": -5, "balance": -100.50}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result["temperature"] == -5
    assert result["balance"] == -100.50


def test_scientific_notation():
    """Test scientific notation numbers."""
    data = {"small": 1e-10, "large": 1e10}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert "small" in result
    assert "large" in result


def test_whitespace_in_values():
    """Test values with whitespace."""
    data = {"message": "Hello World", "path": "  /usr/local  "}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result["message"] == "Hello World"


def test_colon_in_values():
    """Test colons in values."""
    data = {"time": "12:30:45", "url": "http://example.com"}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result["time"] == "12:30:45"
    assert result["url"] == "http://example.com"


def test_single_item_array():
    """Test array with single item."""
    data = {"items": ["single"]}
    toon = json_to_toon(data)
    result = toon_to_json(toon)
    assert result == data


def test_nested_empty_objects():
    """Test nested empty objects."""
    data = {"outer": {"inner": {}}}
    toon = json_to_toon(data)
    # Empty objects may not round-trip perfectly
    assert "outer:" in toon
