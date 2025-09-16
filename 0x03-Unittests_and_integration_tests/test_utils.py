#!/usr/bin/env python3
"""
Unit tests for utils module.
Tests the `access_nested_map` function using parameterized test cases.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: dict,
                               path: tuple,
                               expected: object) -> None:
        """
        Test that access_nested_map returns correct value for given paths.

        Args:
            nested_map (dict): The nested dictionary to search.
            path (tuple): The tuple of keys to access.
            expected (object): The expected value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
