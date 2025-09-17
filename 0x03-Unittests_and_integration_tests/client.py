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

    def public_repos(self, license: str = None) -> List[str]:
        """
        Return a list of public repo names for the organization.
        Optionally filter by license.
        """
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        
        return [
            repo["name"] for repo in repos 
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict[str, Any], license_key: str) -> bool:
        """
        Check if a repository has a specific license.
        """
        license_info = repo.get("license")
        if license_info is None:
            return False
        return license_info.get("key") == license_key
