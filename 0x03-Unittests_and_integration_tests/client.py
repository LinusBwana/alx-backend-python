#!/usr/bin/env python3
"""
client module
Contains GithubOrgClient class to interact with GitHub API.
"""

from utils import get_json


class GithubOrgClient:
    """
    GithubOrgClient class
    """

    def __init__(self, org_name: str) -> None:
        """
        Initialize the client with the organization name.
        """
        self._org_name = org_name

    @property
    def org(self):
        """
        Returns the organization data from GitHub.
        """
        return get_json(f"https://api.github.com/orgs/{self._org_name}")
