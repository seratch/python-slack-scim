import random
import string
import unittest

import pytest

from slack_scim import Users, User, SCIMClient, SCIMApiError
from tests.v1 import load_token
from tests.v1.mock_server import setup_mock_server, cleanup_mock_server


class TestUsers(unittest.TestCase):
    def setUp(self):
        setup_mock_server(self)
        # `admin` scope required
        self.token = load_token()
        base_url = self.server_url or SCIMClient.production_base_url
        self.client = SCIMClient(token=self.token, base_url=base_url)

    def tearDown(self):
        cleanup_mock_server(self)

    def test_search_users_error(self):
        client = SCIMClient(token="")
        with pytest.raises(
            SCIMApiError,
            match=r"'errors': {'description': 'invalid_authentication', 'code': 401}"):
            client.search_users(count=3)

    def test_search_and_read_users(self):
        search_result: Users = self.client.search_users(count=3)
        search_result is not None
        assert search_result.start_index == 1
        assert len(search_result.resources) == 3

        user = search_result.resources[1]
        assert user.name.given_name is not None

        read_result: User = self.client.read_user(user.id)
        assert user.to_dict() == read_result.to_dict()

        search_result: Users = self.client.search_users(count=2, start_index=2)
        assert search_result.start_index == 2
        assert len(search_result.resources) == 2
        assert search_result.resources[0].id == user.id

    def test_user_crud(self):
        random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        new_user: User = User.from_dict({
            "name": {
                "givenName": "Kazuhiro",
                "familyName": "Sera",
            },
            "emails": [{"value": f"test-{random_str}@example.com"}],
            "userName": f"slack_scim-{random_str}",
        })
        creation_result: User = self.client.create_user(new_user)
        user_id = creation_result.id

        patch_result: User = self.client.patch_user(user_id, {
            "name": {
                "givenName": "Kaz"
            }
        })
        assert patch_result.name.given_name == "Kaz"

        patch_result.name.given_name = "K"
        update_result = self.client.update_user(user_id, patch_result)
        assert update_result.name.given_name == "K"

        self.client.delete_user(user_id)
