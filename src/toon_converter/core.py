"""Core conversion functions for JSON <-> TOON."""

import json
from typing import Any, Union
from .exceptions import TOONParseError


def json_to_toon(data: Union[dict, list, str], indent: int = 2) -> str:
    """Convert JSON to TOON format.
    
    Args:
        data: JSON data (dict, list, or JSON string)
        indent: Number of spaces for indentation
        
    Returns:
        TOON formatted string
    """
    if isinstance(data, str):
        data = json.loads(data)
    
    # Pre-check for simple types
    if data is None: return "null"
    if isinstance(data, bool): return "true" if data else "false"
    if isinstance(data, (int, float)): return str(data)
    if isinstance(data, str): return data
    if not data: return ""

    lines = []
    # Stack: (obj, level, prefix)
    # prefix is the string to print before the object (e.g. "key:" or "-")
    # If prefix is None, it means just print the object at 'level' indentation.
    
    stack = [(data, 0, None)]
    
    while stack:
        obj, level, prefix = stack.pop()
        
        if isinstance(obj, dict):
            if not obj:
                # Empty dict
                val_str = "{}"
                if prefix:
                    lines.append(f"{prefix} {val_str}")
                else:
                    spacing = " " * (level * indent)
                    lines.append(f"{spacing}{val_str}")
                continue

            if prefix:
                lines.append(prefix)
                child_level = level + 1
            else:
                child_level = level
            
            # Push items in reverse order
            for key, value in reversed(list(obj.items())):
                key_str = f'"{key}"' if ":" in key else key
                spacing = " " * (child_level * indent)
                child_prefix = f"{spacing}{key_str}:"
                stack.append((value, child_level, child_prefix))
                    
        elif isinstance(obj, list):
            if not obj:
                # Empty list
                val_str = "[]"
                if prefix:
                    lines.append(f"{prefix} {val_str}")
                else:
                    spacing = " " * (level * indent)
                    lines.append(f"{spacing}{val_str}")
                continue

            if prefix:
                lines.append(prefix)
                child_level = level + 1
            else:
                child_level = level
            
            for i in range(len(obj) - 1, -1, -1):
                item = obj[i]
                
                if isinstance(item, dict) and item:
                    spacing = " " * (child_level * indent)
                    child_prefix = f"{spacing}-"
                    stack.append((item, child_level, child_prefix))
                else:
                    # Simple value or list in list
                    stack.append((item, child_level, None))
        
        else:
            # Simple value
            val_str = _simple_value_to_string(obj)
            if prefix:
                lines.append(f"{prefix} {val_str}")
            else:
                spacing = " " * (level * indent)
                lines.append(f"{spacing}{val_str}")
        
    return "\n".join(lines)


def _simple_value_to_string(obj: Any) -> str:
    if obj is None: return "null"
    if isinstance(obj, bool): return "true" if obj else "false"
    return str(obj)


def toon_to_json(toon_str: str) -> Union[dict, list]:
    """Convert TOON format to JSON.
    
    Args:
        toon_str: TOON formatted string
        
    Returns:
        Parsed JSON data (dict or list)
    """
    lines = [line for line in toon_str.strip().split("\n") if line.strip()]
    if not lines:
        return {}
    
    root = {}
    # Stack: (container, indent_level)
    stack = [(root, -1)]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        
        # Pop stack if we went back in indentation
        while len(stack) > 1 and indent <= stack[-1][1]:
            stack.pop()
            
        current_container = stack[-1][0]
        
        # Handle array item marker
        if stripped == "-":
            # Start of object in array
            if isinstance(current_container, list):
                new_obj = {}
                current_container.append(new_obj)
                stack.append((new_obj, indent))
                i += 1
                continue
            else:
                # Should not happen
                pass
        
        # Handle quoted keys
        key = None
        value_str = None
        has_colon = False
        
        if stripped.startswith('"'):
            end_quote = stripped.find('"', 1)
            if end_quote != -1 and end_quote + 1 < len(stripped) and stripped[end_quote+1] == ':':
                key = stripped[1:end_quote]
                value_str = stripped[end_quote+2:].strip()
                has_colon = True
        
        if not has_colon and ":" in stripped:
            key, _, value_str = stripped.partition(":")
            key = key.strip()
            value_str = value_str.strip()
            has_colon = True
            
        if has_colon:
            if value_str:
                val = _parse_value(value_str)
                if isinstance(current_container, dict):
                    current_container[key] = val
                elif isinstance(current_container, list):
                    # Legacy: object in list without '-'
                    if current_container and current_container[-1] is not None and isinstance(current_container[-1], dict) and key not in current_container[-1]:
                        current_container[-1][key] = val
                    else:
                        current_container.append({key: val})
            else:
                # Nested structure or None
                # Look ahead to determine if there are children
                has_children = False
                next_type = dict
                
                if i + 1 < len(lines):
                    next_line_content = lines[i+1]
                    next_indent = len(next_line_content) - len(next_line_content.lstrip())
                    
                    # Must be more indented to be a child
                    # Note: current indent is 'indent'. 
                    # But wait, 'indent' variable is indentation of CURRENT line.
                    # If we are in a dict, children should be indented relative to current line?
                    # Yes.
                    
                    if next_indent > indent:
                        has_children = True
                        stripped_next = next_line_content.strip()
                        if stripped_next == "-" or (":" not in stripped_next and not stripped_next.startswith('"')):
                             if ":" not in stripped_next and not stripped_next.startswith('"'):
                                  next_type = list
                
                if has_children:
                    new_container = next_type()
                    if isinstance(current_container, dict):
                        current_container[key] = new_container
                    elif isinstance(current_container, list):
                        if current_container and current_container[-1] is not None and isinstance(current_container[-1], dict) and key not in current_container[-1]:
                            current_container[-1][key] = new_container
                        else:
                            current_container.append({key: new_container})
                            new_container = current_container[-1][key]
                    
                    stack.append((new_container, indent))
                else:
                    # No children -> None
                    if isinstance(current_container, dict):
                        current_container[key] = None
                    elif isinstance(current_container, list):
                        if current_container and current_container[-1] is not None and isinstance(current_container[-1], dict) and key not in current_container[-1]:
                            current_container[-1][key] = None
                        else:
                            current_container.append({key: None})
        else:
            # Simple value in array
            val = _parse_value(stripped)
            if isinstance(current_container, list):
                current_container.append(val)
            elif isinstance(current_container, dict):
                # Key without value?
                pass
                
        i += 1
        
    return root


def _parse_value(value: str) -> Any:
    """Parse a value string to appropriate type."""
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    
    # Try number (only if it looks like a pure number)
    try:
        # Fix: Don't parse as number if it has leading zeros (unless it's just "0" or "0.xxx")
        if value.startswith("0") and len(value) > 1 and value[1] != ".":
            return value

        if value.replace(".", "", 1).replace("-", "", 1).replace("e", "", 1).replace("E", "", 1).replace("+", "", 1).isdigit():
            if "." in value or "e" in value.lower():
                return float(value)
            return int(value)
    except (ValueError, AttributeError):
        pass
    
    return value
