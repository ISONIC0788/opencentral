# Utility functions for the LogMachine backend.

def stringify(obj):
    """
    Recursively convert all non-primitive types in the given object to strings for JSON serialization.
    """
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = stringify(value)
        return obj
    if isinstance(obj, list):
        return [stringify(item) for item in obj]
    if isinstance(obj, set):
        return {stringify(item) for item in obj}
    if isinstance(obj, tuple):
        return tuple(stringify(item) for item in obj)
    return str(obj)
