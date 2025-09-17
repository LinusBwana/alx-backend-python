#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"org": "google"}),
        ("abc", {"org": "abc"}),
    ])
    @patch('client.get_json', return_value={"org": "test"})
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the expected result.
        """
        client = GithubOrgClient(org_name)
        result = client.org

        # Ensure get_json is called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Ensure returned result matches the mocked payload
        self.assertEqual(result, {"org": "test"})

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL from mocked org property"""
        fake_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test_org")

        # Patch the `org` property using a context manager
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = fake_payload

            result = client._public_repos_url
            expected = fake_payload["repos_url"]

            # Verify the property returns the expected repos URL
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
