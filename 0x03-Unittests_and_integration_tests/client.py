#!/usr/bin/env python3
"""
client module
Contains GithubOrgClient class to interact with GitHub API.
"""

from typing import Dict, Any, List
from utils import get_json


class GithubOrgClient:
    """
    GithubOrgClient class to interact with GitHub organizations.
    """

    def __init__(self, org_name: str) -> None:
        """
        Initialize the client with the organization name.
        """
        self._org_name = org_name

    @property
    def org(self) -> Dict[str, Any]:
        """
        Fetch and return organization data from GitHub.
        """
        return get_json(f"https://api.github.com/orgs/{self._org_name}")

    @property
    def _public_repos_url(self) -> str:
        """
        Return the public repos URL from the organization payload.
        """
        return self.org.get("repos_url")

    def public_repos(self) -> List[str]:
        """
        Return a list of public repo names for the organization.
        """
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]
