"""Validation functions for JSON and TOON formats."""

import json
from typing import Tuple
from .exceptions import JSONValidationError, TOONValidationError


def validate_json(data: str) -> Tuple[bool, str]:
    """Validate JSON string.
    
    Args:
        data: JSON string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        json.loads(data)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
    except Exception as e:
        return False, f"JSON validation error: {str(e)}"


def validate_toon(data: str) -> Tuple[bool, str]:
    """Validate TOON string.
    
    Args:
        data: TOON string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if not data or not data.strip():
            return False, "Empty TOON data"
        
        lines = data.strip().split("\n")
        
        prev_indent = 0
        indent_stack = [0]
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            indent = len(line) - len(line.lstrip())
            
            # Check indent is multiple of 2
            if indent % 2 != 0:
                return False, f"Line {line_num}: Invalid indentation (must be multiple of 2 spaces)"
            
            # Check indent doesn't jump more than one level
            if indent > prev_indent and indent - prev_indent > 2:
                return False, f"Line {line_num}: Indentation jumps more than one level"
            
            # Update indent stack
            while indent_stack and indent < indent_stack[-1]:
                indent_stack.pop()
            
            if indent > prev_indent:
                indent_stack.append(indent)
            
            prev_indent = indent
            
            stripped = line.strip()
            
            # Check for valid key-value format
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                if not key.strip():
                    return False, f"Line {line_num}: Empty key before colon"
        
        return True, ""
        
    except Exception as e:
        return False, f"TOON validation error: {str(e)}"


def get_error_details(error: Exception) -> dict:
    """Extract detailed error information.
    
    Args:
        error: Exception object
        
    Returns:
        Dictionary with error details
    """
    details = {
        "type": type(error).__name__,
        "message": str(error)
    }
    
    if hasattr(error, "line_number"):
        details["line_number"] = error.line_number
    
    if hasattr(error, "column"):
        details["column"] = error.column
    
    if isinstance(error, json.JSONDecodeError):
        details["line_number"] = error.lineno
        details["column"] = error.colno
        details["position"] = error.pos
    
    return details
