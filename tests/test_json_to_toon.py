"""Tests for JSON to TOON conversion."""

import pytest
from toon_converter import json_to_toon


def test_simple_object():
    """Test simple object conversion."""
    data = {"name": "Alice", "age": 30}
    result = json_to_toon(data)
    assert "name: Alice" in result
    assert "age: 30" in result


def test_nested_object():
    """Test nested object conversion."""
    data = {
        "user": {
            "name": "Alice",
            "profile": {
                "age": 30
            }
        }
    }
    result = json_to_toon(data)
    assert "user:" in result
    assert "name: Alice" in result
    assert "profile:" in result
    assert "age: 30" in result


def test_array():
    """Test array conversion."""
    data = {"items": ["apple", "banana", "orange"]}
    result = json_to_toon(data)
    assert "items:" in result
    assert "apple" in result
    assert "banana" in result
    assert "orange" in result


def test_mixed_types():
    """Test mixed data types."""
    data = {
        "string": "text",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null_value": None
    }
    result = json_to_toon(data)
    assert "string: text" in result
    assert "number: 42" in result
    assert "float: 3.14" in result
    assert "boolean: true" in result
    assert "null_value: null" in result


def test_empty_object():
    """Test empty object."""
    data = {}
    result = json_to_toon(data)
    assert result == ""


def test_empty_array():
    """Test empty array."""
    data = {"items": []}
    result = json_to_toon(data)
    assert "items:" in result


def test_array_of_objects():
    """Test array containing objects."""
    data = {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
    }
    result = json_to_toon(data)
    assert "users:" in result
    assert "name: Alice" in result
    assert "name: Bob" in result


def test_deep_nesting():
    """Test deeply nested structure."""
    data = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "value": "deep"
                    }
                }
            }
        }
    }
    result = json_to_toon(data)
    assert "level1:" in result
    assert "level2:" in result
    assert "level3:" in result
    assert "level4:" in result
    assert "value: deep" in result


def test_special_characters_in_values():
    """Test special characters in string values."""
    data = {"message": "Hello: World!", "path": "/usr/local/bin"}
    result = json_to_toon(data)
    assert "message: Hello: World!" in result
    assert "path: /usr/local/bin" in result


def test_json_string_input():
    """Test JSON string as input."""
    json_str = '{"name": "Alice", "age": 30}'
    result = json_to_toon(json_str)
    assert "name: Alice" in result
    assert "age: 30" in result


def test_custom_indent():
    """Test custom indentation."""
    data = {"parent": {"child": "value"}}
    result = json_to_toon(data, indent=4)
    lines = result.split("\n")
    # Check that child line has 4 spaces
    child_line = [l for l in lines if "child" in l][0]
    assert child_line.startswith("    ")


def test_boolean_values():
    """Test boolean conversion."""
    data = {"enabled": True, "disabled": False}
    result = json_to_toon(data)
    assert "enabled: true" in result
    assert "disabled: false" in result


def test_numeric_array():
    """Test array of numbers."""
    data = {"numbers": [1, 2, 3, 4, 5]}
    result = json_to_toon(data)
    assert "numbers:" in result
    assert "1" in result
    assert "5" in result


def test_mixed_array():
    """Test array with mixed types."""
    data = {"mixed": ["text", 42, True, None]}
    result = json_to_toon(data)
    assert "mixed:" in result
    assert "text" in result
    assert "42" in result
    assert "true" in result
    assert "null" in result
