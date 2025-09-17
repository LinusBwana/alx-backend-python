#!/usr/bin/env python3
"""
utils module
This module contains utility functions for nested dictionary access,
HTTP JSON fetching, and memoization.
"""

from typing import Any, Dict, Tuple
import requests


def access_nested_map(nested_map: Dict[str, Any], path: Tuple[str, ...]) -> Any:
    """
    Access a nested dictionary using a tuple of keys.

    Args:
        nested_map (Dict[str, Any]): The nested dictionary to access.
        path (Tuple[str, ...]): A tuple representing the sequence of keys.

    Returns:
        Any: The value found at the specified path.

    Raises:
        KeyError: If a key in the path does not exist.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, dict):
            raise KeyError(f"{key} not found in nested map")
        current = current[key]  # Raises KeyError if key does not exist
    return current


def get_json(url: str) -> Dict[str, Any]:
    """
    Fetch JSON data from a given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(method):
    """
    Decorator to cache the result of a method or property.
    """
    attr_name = "_memoized_" + method.__name__

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return property(wrapper)

