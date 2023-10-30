#!/usr/bin/env python3
""" test_utils.py """
import unittest
from client import GithubOrgClient
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import PropertyMock, patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """ TestAccessNestedMap """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ test_access_nested_map """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ test_access_nested_map_exception """
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(error.exception))


class TestGetJson(unittest.TestCase):
    """ TestGetJson """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """ test_get_json """
        mock = Mock()
        mock.json.return_value = test_payload
        with patch('requests.get', return_value=mock):
            self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """ TestMemoize """

    def test_memoize(self):
        """ test_memoize """
        class TestClass:
            """ TestClass """

            def a_method(self):
                """ a_method """
                return 42

            @memoize
            def a_property(self):
                """ a_property """
                return self.a_method()
        with patch.object(TestClass, 'a_method', return_value=42) as mock:
            test = TestClass()
            test.a_property
            test.a_property
            mock.assert_called_once()


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
    