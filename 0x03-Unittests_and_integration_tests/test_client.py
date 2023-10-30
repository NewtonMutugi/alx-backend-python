#!/usr/bin/env python3
""" test_client.py """

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, test_org, mock):
        """ test_org """
        test = GithubOrgClient(test_org)
        test.org()
        mock.assert_called_once_with(f"https://api.github.com/orgs/{test_org}")

    def test_public_repos_url(self):
        """ test_public_repos_url """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            test = GithubOrgClient("test")
            test.org()
            mock.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock):
        """ test_public_repos """
        payload = [{"name": "Google"}, {"name": "abc"}]
        mock.return_value = payload
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public:
            mock_public.return_value = "test"
            test = GithubOrgClient("test")
            self.assertEqual(test._public_repos_url, "test")
            self.assertEqual(test.public_repos(), ["Google", "abc"])
            mock.assert_called_once_with("test")

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """ test_has_license """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)
