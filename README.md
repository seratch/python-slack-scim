# slack-scim - Slack SCIM API Client

[![PyPI version](https://badge.fury.io/py/slack-scim.svg)](https://badge.fury.io/py/slack-scim) [![Build Status](https://travis-ci.org/seratch/python-slack-scim.svg?branch=master)](https://travis-ci.org/seratch/python-slack-scim)

This library provides ways to call Slack's SCIM APIs in the Pythonic way.

* [SCIM (System for Cross-domain Identity Management)](http://www.simplecloud.info/)
* [Slack SCIM API](https://api.slack.com/scim)

## Getting Started

It's pretty easy and intuitive to use this library 😉 Try with your admin user token!

```bash
$ pip install slack-scim
Collecting slack-scim
  Using cached slack_scim-1.0.5-py2.py3-none-any.whl (20 kB)
Installing collected packages: slack-scim
Successfully installed slack-scim-1.0.5

$ python

>>> import os
>>> import slack_scim
>>> client = slack_scim.SCIMClient(token=os.environ["SLACK_ADMIN_TOKEN"])

>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> users = client.search_users(filter="restricted eq 1", count=5)
DEBUG:slack_scim.v1.client:*** SCIM API Request ***
GET https://api.slack.com/scim/v1/Users?filter=restricted+eq+1&count=5
Authorization: (redacted)
Content-type: application/x-www-form-urlencoded;charset=utf-8


DEBUG:slack_scim.v1.client:*** SCIM API Response ***
GET https://api.slack.com/scim/v1/Users?filter=restricted+eq+1&count=5
200 OK
date: Sun, 26 Apr 2020 03:53:44 GMT
server: Apache
strict-transport-security: max-age=31536000; includeSubDomains; preload
referrer-policy: no-referrer
x-slack-backend: h
vary: Accept-Encoding
x-xss-protection: 0
x-frame-options: SAMEORIGIN
connection: close
transfer-encoding: chunked
content-type: application/json; charset=utf-8
x-via: haproxy-www-4mte

{"totalResults":2,"itemsPerPage":2,"startIndex":1,"schemas":["urn:scim:schemas:core:1.0"],"Resources":[{"schemas":["urn:scim:schemas:core:1.0"],"id":"WRDCW4CHX","externalId":"","meta":{"created":"2019-12-14T01:26:43-08:00","location":"https:\/\/api.slack.com\/scim\/v1\/Users\/WRDCW4CHX"},"userName":"steve","nickName":"steve","name":{"givenName":"Hiroyuki","familyName":"Aoki"},"displayName":"steve","profileUrl":"https:\/\/your-domain.enterprise.slack.com\/team\/Steve Aoki","title":"","timezone":"America\/Los_Angeles","active":true,"emails":[{"value":"saoki@example.com","primary":true}],"photos":[{"value":"https:\/\/secure.gravatar.com\/avatar\/111.jpg","type":"photo"}],"groups":[]},{"schemas":["urn:scim:schemas:core:1.0"],"id":"W0107TELUM7","externalId":"","meta":{"created":"2020-03-22T17:38:28-07:00","location":"https:\/\/api.slack.com\/scim\/v1\/Users\/W0107TELUM7"},"userName":"will.i.am","nickName":"will.i.am","name":{"givenName":"William","familyName":"Adams"},"displayName":"will.i.am","profileUrl":"https:\/\/your-domain.enterprise.slack.com\/team\/will.i.am","title":"","timezone":"America\/Los_Angeles","active":true,"emails":[{"value":"will-i-am@example.com","primary":true}],"photos":[{"value":"https:\/\/secure.gravatar.com\/avatar\/222.jpg","type":"photo"}],"groups":[]}]}

>>> users.
users.active          users.external_id     users.id              users.name            users.profile_url     users.start_index     users.to_dict(        
users.display_name    users.from_dict(      users.items_per_page  users.nick_name       users.resources       users.timezone        users.total_results   
users.emails          users.groups          users.meta            users.photos          users.schemas         users.title           users.user_name

>>> list(map(lambda u: u.id, users.resources))
['WRDCW4CHX', 'W0107TELUM7']

>>> list(map(lambda u: u.to_dict()["name"], users.resources))
[{'familyName': 'Aoki', 'givenName': 'Steve'}, {'familyName': 'Adams', 'givenName': 'Adams'}]
```

## Basics

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

## License

The MIT License
