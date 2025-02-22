import json


def is_json_serialized(value: str) -> bool:
    """
    Check if a string is a valid JSON
    """
    if not isinstance(value, str):
        return False
    try:
        json.loads(value)
        return True
    except json.JSONDecodeError:
        return False
