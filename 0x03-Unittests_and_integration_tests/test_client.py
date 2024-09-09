#!/usr/bin/env python3
'''Unittests for client module'''
import unittest
from typing import Dict
from parameterized import parameterized
from unittest.mock import (
    patch,
    PropertyMock,
    MagicMock,
)

from client import GithubOrgClient


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
