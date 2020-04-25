# slack-scim - Slack SCIM API Client

[![PyPI version](https://badge.fury.io/py/slack-scim.svg)](https://badge.fury.io/py/slack-scim) [![Build Status](https://travis-ci.org/seratch/pyton-slack-scim.svg?branch=master)](https://travis-ci.org/seratch/pyton-slack-scim)

This library provides ways to call Slack's SCIM APIs in the Pythonic way.

* [SCIM (System for Cross-domain Identity Management)](http://www.simplecloud.info/)
* [Slack SCIM API](https://api.slack.com/scim)

## Getting Started

### Installation

```bash
pip install slack-scim
```

### User Management

https://api.slack.com/scim#users

```python
import os
from slack_scim import Users, User
from slack_scim import SCIMClient, SCIMApiError

# `admin` scope required
token = os.environ["SLACK_ADMIN_TOKEN"]
client = SCIMClient(token=token)
try:
    search_result: Users = client.search_users(filter="restricted eq '1'", count=3)
    user_id = search_result.resources[0].id
    read_result: User = client.read_user(user_id)
except SCIMApiError as err:
    if err.status == 429:
        # handle rate limit errors
        pass

new_user: User = User.from_dict({
    "name": {
        "givenName": "Kazuhiro",
        "familyName": "Sera",
    },
    "emails": [{"value": "your-name@example.com"}],
    "userName": "seratch",
})
creation_result: User = client.create_user(new_user)
user_id = creation_result.id

patch_result: User = client.patch_user(user_id, {
    "name": {
        "givenName": "Kaz"
    }
})

patch_result.name.given_name = "K"
update_result: User = client.update_user(user_id, patch_result)

client.delete_user(user_id)
```

### Group Management

https://api.slack.com/scim#groups

```python
import os
from slack_scim import Groups, Group, GroupMember, SCIMClient, User

# `admin` scope required
token = os.environ["SLACK_ADMIN_TOKEN"]
client = SCIMClient(token=token)

display_name = "test-group-123"
new_group: Group = Group.from_dict({"displayName": display_name})
created_user: User = client.create_user(User.from_dict({
    "name": {
        "givenName": "Kazuhiro",
        "familyName": "Sera",
    },
    "emails": [{"value": "your-name@example.com"}],
    "userName": "seratch",
}))
new_group.members = [GroupMember.from_dict(created_user.to_dict())]
creation_result: Group = client.create_group(new_group)
if not creation_result:
    search_result: Groups = client.search_groups(filter=f"displayName eq {display_name}", count=1)
    creation_result: Group = search_result.resources[0]
group_id = creation_result.id

client.patch_group(group_id, {"displayName": display_name + "-2"})
patch_result: Group = client.read_group(group_id)

patch_result.display_name = display_name + "-3"
client.update_group(group_id, patch_result)
update_result = client.read_group(group_id)

client.delete_group(group_id)
```

## Contribution

Your contributions are always welcome! Before submitting a pull request, verify your code works with Slack SCIM APIs.

```bash
export SLACK_ADMIN_TOKEN=xoxp-***
SLACK_SCIM_TEST_MODE=prod python setup.py test
```

## Deployment

```bash
# https://packaging.python.org/guides/using-testpypi/
pip install twine wheel
rm -rf dist/
python setup.py sdist bdist_wheel
twine check dist/*

# Testing
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ slack-scim

# Deployment
twine upload dist/*
```

## License

The MIT License