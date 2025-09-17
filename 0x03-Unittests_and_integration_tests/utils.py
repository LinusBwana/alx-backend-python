#!/usr/bin/env python3
"""
Utility functions for nested map access and JSON fetching.
"""

import requests


def access_nested_map(nested_map, path):
    """
    Access a nested dictionary using a sequence of keys.

    Args:
        nested_map (dict): The dictionary to access.
        path (tuple): A sequence of keys to traverse.

    Returns:
        The value found at the end of the path.

    Raises:
        KeyError: If any key is missing or if a non-dict is accessed.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, dict):
            # If the current value is not a dictionary, raise KeyError
            raise KeyError(key)
        current = current[key]  # Raises KeyError automatically if key doesn't exist
    return current


def get_json(url):
    """
    Fetch JSON content from a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        dict: The JSON response.
    """
    response = requests.get(url)
    return response.json()


