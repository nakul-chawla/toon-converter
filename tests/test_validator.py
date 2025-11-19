"""Tests for validation functions."""

import pytest
from toon_converter import validate_json, validate_toon, get_error_details
from toon_converter.exceptions import TOONParseError
import json


def test_validate_valid_json():
    """Test validation of valid JSON."""
    valid_json = '{"name": "Alice", "age": 30}'
    is_valid, error = validate_json(valid_json)
    assert is_valid is True
    assert error == ""


def test_validate_invalid_json():
    """Test validation of invalid JSON."""
    invalid_json = '{"name": "Alice", "age": }'
    is_valid, error = validate_json(invalid_json)
    assert is_valid is False
    assert "Invalid JSON" in error


def test_validate_malformed_json():
    """Test validation of malformed JSON."""
    malformed = '{"name": "Alice"'
    is_valid, error = validate_json(malformed)
    assert is_valid is False
    assert error != ""


def test_validate_valid_toon():
    """Test validation of valid TOON."""
    valid_toon = """name: Alice
age: 30"""
    is_valid, error = validate_toon(valid_toon)
    assert is_valid is True
    assert error == ""


def test_validate_nested_toon():
    """Test validation of nested TOON."""
    valid_toon = """user:
  name: Alice
  profile:
    age: 30"""
    is_valid, error = validate_toon(valid_toon)
    assert is_valid is True
    assert error == ""


def test_validate_empty_toon():
    """Test validation of empty TOON."""
    is_valid, error = validate_toon("")
    assert is_valid is False
    assert "Empty" in error


def test_validate_invalid_indentation():
    """Test validation with invalid indentation."""
    invalid_toon = """name: Alice
 age: 30"""  # 1 space instead of 2
    is_valid, error = validate_toon(invalid_toon)
    assert is_valid is False
    assert "indentation" in error.lower()


def test_validate_empty_key():
    """Test validation with empty key."""
    invalid_toon = """: value"""
    is_valid, error = validate_toon(invalid_toon)
    assert is_valid is False
    assert "Empty key" in error


def test_get_error_details_json():
    """Test error details extraction from JSON error."""
    try:
        json.loads('{"invalid": }')
    except json.JSONDecodeError as e:
        details = get_error_details(e)
        assert "type" in details
        assert "message" in details
        assert "line_number" in details


def test_get_error_details_toon():
    """Test error details extraction from TOON error."""
    error = TOONParseError("Test error", line_number=5, column=10)
    details = get_error_details(error)
    assert details["type"] == "TOONParseError"
    assert details["line_number"] == 5
    assert details["column"] == 10


def test_validate_toon_with_array():
    """Test validation of TOON with arrays."""
    valid_toon = """items:
  apple
  banana"""
    is_valid, error = validate_toon(valid_toon)
    assert is_valid is True


def test_validate_complex_structure():
    """Test validation of complex TOON structure."""
    complex_toon = """config:
  database:
    host: localhost
    port: 5432
  features:
    auth
    logging
  settings:
    timeout: 30
    retries: 3"""
    is_valid, error = validate_toon(complex_toon)
    assert is_valid is True
