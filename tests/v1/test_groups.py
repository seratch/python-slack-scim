import random
import string
import time
import unittest

import pytest

from slack_scim import Groups, Group, GroupMember, SCIMClient, SCIMApiError, User
from tests.v1 import load_token
from tests.v1.mock_server import setup_mock_server, cleanup_mock_server


class TestGroups(unittest.TestCase):
    def setUp(self):
        setup_mock_server(self)
        # `admin` scope required
        self.token = load_token()
        base_url = self.server_url or SCIMClient.production_base_url
        self.client = SCIMClient(token=self.token, base_url=base_url)

    def tearDown(self):
        cleanup_mock_server(self)

    def test_search_groups_error(self):
        client = SCIMClient(token="")
        with pytest.raises(
            SCIMApiError,
            match=r"'errors': {'description': 'invalid_authentication', 'code': 401}"):
            client.search_groups(count=3)

    def test_group(self):
        random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        display_name = f"test-group-{random_str}"
        new_group: Group = Group.from_dict({"displayName": display_name})

        created_user: User = self.client.create_user(User.from_dict({
            "name": {
                "givenName": "Kazuhiro",
                "familyName": "Sera",
            },
            "emails": [{"value": f"test-{random_str}@example.com"}],
            "userName": f"slack_scim-{random_str}",
        }))
        try:
            new_group.members = [GroupMember.from_dict(created_user.to_dict())]
            creation_result: Group = self.client.create_group(new_group)
            if not creation_result:
                search_result = self.client.search_groups(filter=f"displayName eq {display_name}", count=1)
                creation_result = search_result.resources[0]
            display_name = creation_result.display_name
            group_id = creation_result.id
            try:
                patch_result: Group = self.client.patch_group(group_id, {"displayName": f"{display_name}-2"})
                if not patch_result:
                    time.sleep(3)
                    patch_result: Group = self.client.read_group(group_id)
                assert f"{display_name}-2" == patch_result.display_name

                patch_result.display_name = f"{display_name}-3"
                update_result = self.client.update_group(group_id, patch_result)
                if not update_result or f"{display_name}-3" != update_result.display_name:
                    time.sleep(3)
                    update_result = self.client.read_group(group_id)
                assert f"{display_name}-3" == update_result.display_name

                search_result: Groups = self.client.search_groups(count=3)
                search_result is not None
                assert search_result.start_index == 1
                assert len(search_result.resources) == 3

                group = search_result.resources[1]
                self.assertIsNotNone(group.display_name)

                read_result: Group = self.client.read_group(group.id)
                self.assertDictEqual(group.to_dict(), read_result.to_dict())

                search_result: Groups = self.client.search_groups(count=2, start_index=2)
                assert search_result.start_index == 2
                assert len(search_result.resources) == 2
                assert search_result.resources[0].id == group.id
            finally:
                self.client.delete_group(group_id)
        finally:
            self.client.delete_user(created_user.id)

    def test_read_group_members(self):
        group = self.client.read_group("S333")
        assert len(group.members) == 1
        member = group.members[0]
        print(member.__dict__)
        assert member.value == "M333"
        assert member.display == "Michael Jackson"
