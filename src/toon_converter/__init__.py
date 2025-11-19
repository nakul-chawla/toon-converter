"""TOON Converter - Token-Oriented Object Notation for LLM prompts."""

__version__ = "0.1.0"

from .core import json_to_toon, toon_to_json
from .validator import validate_json, validate_toon, get_error_details
from .exceptions import TOONError, TOONParseError, TOONValidationError, JSONValidationError

__all__ = [
    "json_to_toon",
    "toon_to_json",
    "validate_json",
    "validate_toon",
    "get_error_details",
    "TOONError",
    "TOONParseError",
    "TOONValidationError",
    "JSONValidationError",
]
