#!/usr/bin/env python3
"""
utils module
This module contains utility functions for nested dictionary access.
"""


from typing import Any, Mapping, Tuple


def access_nested_map(nested_map: Mapping, path: Tuple[str, ...]) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Args:
        nested_map (Mapping): A dictionary that may contain nested dictionaries.
        path (Tuple[str, ...]): A tuple representing the path of keys to access.

    Returns:
        Any: The value found at the end of the path.

    Raises:
        KeyError: If a key in the path is not found in the map.
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current


if __name__ == "__main__":
    # Simple manual test when running directly
    example = {"a": {"b": 2}}
    print(access_nested_map(example, ("a", "b")))  # Expected output: 2
