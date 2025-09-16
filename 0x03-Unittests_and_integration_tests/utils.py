#!/usr/bin/python3
"""
utils module
This module contains utility functions for nested dictionary access.
"""

from typing import Mapping, Any, Tuple


def access_nested_map(nested_map: Mapping, path: Tuple[str, ...]) -> Any:
    """
    Access a nested dictionary using a tuple path.

    Args:
        nested_map (Mapping): A dictionary that may contain other dictionaries.
        path (Tuple[str, ...]): A tuple representing the keys to access.

    Returns:
        Any: The value found at the end of the path.

    Raises:
        KeyError: If a key in the path is not found.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, dict):
            # Raise a KeyError for the current invalid key
            raise KeyError(key)
        current = current[key]
    return current


