"""Tests for TOON to JSON conversion."""

import pytest
from toon_converter import toon_to_json


def test_simple_object():
    """Test simple object parsing."""
    toon = """name: Alice
age: 30"""
    result = toon_to_json(toon)
    assert result == {"name": "Alice", "age": 30}


def test_nested_object():
    """Test nested object parsing."""
    toon = """user:
  name: Alice
  profile:
    age: 30"""
    result = toon_to_json(toon)
    assert result == {
        "user": {
            "name": "Alice",
            "profile": {"age": 30}
        }
    }


def test_array():
    """Test array parsing."""
    toon = """items:
  apple
  banana
  orange"""
    result = toon_to_json(toon)
    assert result == {"items": ["apple", "banana", "orange"]}


def test_mixed_types():
    """Test mixed data types."""
    toon = """string: text
number: 42
float: 3.14
boolean: true
null_value: null"""
    result = toon_to_json(toon)
    assert result == {
        "string": "text",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null_value": None
    }


def test_empty_string():
    """Test empty input."""
    result = toon_to_json("")
    assert result == {}


def test_numeric_array():
    """Test array of numbers."""
    toon = """numbers:
  1
  2
  3"""
    result = toon_to_json(toon)
    assert result == {"numbers": [1, 2, 3]}


def test_boolean_values():
    """Test boolean parsing."""
    toon = """enabled: true
disabled: false"""
    result = toon_to_json(toon)
    assert result == {"enabled": True, "disabled": False}


def test_null_value():
    """Test null value parsing."""
    toon = """value: null"""
    result = toon_to_json(toon)
    assert result == {"value": None}


def test_empty_value():
    """Test empty value (key with no value)."""
    toon = """key:"""
    result = toon_to_json(toon)
    assert result == {"key": None}


def test_deep_nesting():
    """Test deeply nested structure."""
    toon = """level1:
  level2:
    level3:
      level4:
        value: deep"""
    result = toon_to_json(toon)
    assert result == {
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


def test_multiple_arrays():
    """Test multiple arrays."""
    toon = """fruits:
  apple
  banana
colors:
  red
  blue"""
    result = toon_to_json(toon)
    assert result == {
        "fruits": ["apple", "banana"],
        "colors": ["red", "blue"]
    }


def test_mixed_array():
    """Test array with mixed types."""
    toon = """mixed:
  text
  42
  true
  null"""
    result = toon_to_json(toon)
    assert result == {"mixed": ["text", 42, True, None]}


def test_special_characters():
    """Test special characters in values."""
    toon = """message: Hello: World!
path: /usr/local/bin"""
    result = toon_to_json(toon)
    assert result == {
        "message": "Hello: World!",
        "path": "/usr/local/bin"
    }


def test_whitespace_handling():
    """Test handling of extra whitespace."""
    toon = """name: Alice  
age: 30  """
    result = toon_to_json(toon)
    assert result == {"name": "Alice", "age": 30}


def test_float_numbers():
    """Test float number parsing."""
    toon = """pi: 3.14159
ratio: 0.5"""
    result = toon_to_json(toon)
    assert result == {"pi": 3.14159, "ratio": 0.5}


def test_negative_numbers():
    """Test negative number parsing."""
    toon = """temperature: -5
balance: -100.50"""
    result = toon_to_json(toon)
    assert result == {"temperature": -5, "balance": -100.50}
