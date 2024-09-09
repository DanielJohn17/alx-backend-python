#!/usr/bin/env python3
'''Unittests for client module'''
import unittest
from typing import Dict
from parameterized import parameterized, parameterized_class
from unittest.mock import (
    patch,
    PropertyMock,
    MagicMock,
    Mock,
)
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    '''TestGithubOrgClient class'''

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        '''Test org method'''
        mocked_fxn.return_value = MagicMock(return_value=resp)
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org(), resp)
        mocked_fxn.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        '''Test _public_repos_url property'''
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mocked_org:
            mocked_org.return_value = {
                "repos_url": "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        '''Test public_repos method'''
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "id": 12345,
                    "name": "python_test",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 52369,
                    },
                },
                {
                    "id": 25345,
                    "name": "shell_test",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 52369,
                    },
                }
            ]
        }

        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_publick_repos_url:
            mock_publick_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "python_test",
                    "shell_test",
                ],
            )
            mock_publick_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
    ])
    def test_has_license(
            self,
            repo: Dict,
            license_key: str,
            expected: bool
    ) -> None:
        '''Test has_license method'''
        gh_org_client = GithubOrgClient("google")
        client_has_license = gh_org_client.has_license(repo, license_key)
        self.assertEqual(client_has_license, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Integration test for GithubOrgClient'''
    @classmethod
    def setUpClass(cls) -> None:
        '''Set up class'''
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        '''Test public_repos method'''
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        '''Test public_repos method with license'''
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        '''Tear down class'''
        cls.get_patcher.stop()
