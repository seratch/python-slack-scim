import copy
import json
import logging
from http.client import HTTPResponse
from typing import Union
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

from .errors import SCIMApiError, SCIMError
from .group import Group
from .groups import Groups
from .request import SCIMRequest
from .response import SCIMResponse
from .service_provider_configs import ServiceProviderConfigs
from .user import User
from .users import Users


class SCIMClient:
    _logger = logging.getLogger(__name__)

    production_base_url = "https://api.slack.com/scim/v1"
    schema_values = [
        "urn:scim:schemas:core:1.0",
        "urn:scim:schemas:extension:enterprise:1.0"
    ]

    def __init__(
        self,
        token: str,
        base_url: str = production_base_url
    ):
        """Slack SCIM API Client

        https://api.slack.com/scim

        As this class doesn't have any other state apart from the token and base_Url, if your app is fine with
        reusing the same settings for requests, you can use an instance as singleton in your app.s

        :param token: An OAuth token with the admin scope is required to access the SCIM API.
            The simplest way to acquire this token is for an admin on a Workspace to create a new Slack app,
            add the admin OAuth scope, install the app, and use the generated token.
        :param base_url: the default one is the production URL. If you want to use proxy URL or test server URL,
            Give the URL to this parameter.
        """
        self.token: str = token
        self.base_url: str = base_url

    def __repr__(self):
        d: dict = {"token": "(redacted)", "base_url": self.base_url}
        return f"<slack_scim.{self.__class__.__name__}: {d}>"

    # ----------------------------------------------
    # User Management
    # ----------------------------------------------

    def create_user(
        self,
        user: Union[dict, User]
    ) -> User:
        """Creates a new user.

        https://api.slack.com/scim#users

        :param user: if you give a dict value here, be noted that keys must be camel-cased,
            not your familiar snake-case style.
        """
        req = SCIMRequest(
            token=self.token,
            http_method="POST",
            url=f"{self.base_url}/Users",
            json_body=self._to_user_dict(user),
        )
        resp = self.api_call(req)
        if resp.is_success():
            return User.from_dict(json.loads(resp.body))
        else:
            raise SCIMApiError.from_response(resp)

    def patch_user(
        self,
        id: str,
        user: Union[dict, User]
    ) -> User:
        """Partially updates a user.

        https://api.slack.com/scim#users

        :param id: user ID
        :param user: if you give a dict value here, be noted that keys must be camel-cased,
            not your familiar snake-case style.
        """
        id = self._ensure_user_id(id, user)
        req = SCIMRequest(
            token=self.token,
            http_method="PATCH",
            url=f"{self.base_url}/Users/{quote(id)}",
            json_body=self._to_user_dict(user),
        )
        resp = self.api_call(req)
        if resp.is_success():
            return User.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def update_user(
        self,
        id: str,
        user: Union[dict, User],
    ) -> User:
        """Overwrites the whole user data.

        https://api.slack.com/scim#users

        :param id: user ID
        :param user: if you give a dict value here, be noted that keys must be camel-cased,
            not your familiar snake-case style.
        """
        id = self._ensure_user_id(id, user)
        req = SCIMRequest(
            token=self.token,
            http_method="PUT",
            url=f"{self.base_url}/Users/{quote(id)}",
            json_body=self._to_user_dict(user),
        )
        resp = self.api_call(req)
        if resp.status == 200:
            return User.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def delete_user(
        self,
        id: str,
    ) -> User:
        """Deletes a user.

        https://api.slack.com/scim#users

        :param id: user ID
        """
        req = SCIMRequest(
            token=self.token,
            http_method="DELETE",
            url=f"{self.base_url}/Users/{quote(id)}",
        )
        resp = self.api_call(req)
        if not resp.is_success():
            raise SCIMApiError.from_response(resp)

    def read_user(
        self,
        id: str,
    ) -> User:
        """Finds a user by user ID.

        https://api.slack.com/scim#users

        :param id: user ID
        """
        req = SCIMRequest(
            token=self.token,
            http_method="GET",
            url=f"{self.base_url}/Users/{quote(id)}",
        )
        resp = self.api_call(req)
        if resp.is_success():
            return User.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def search_users(
        self,
        *,
        filter: str = None,
        count: int = None,
        start_index: int = None
    ) -> Users:
        """Searches the users matching the given filter.

        https://api.slack.com/scim#users

        :param filter: https://api.slack.com/scim#filter
        :param count: the number of results to return in a response
        :param start_index: the index to fetch as the first item
        """
        query = {}
        if filter:
            query["filter"] = filter
        if count:
            query["count"] = count
        if start_index:
            query["startIndex"] = start_index
        req = SCIMRequest(
            token=self.token,
            http_method="GET",
            url=f"{self.base_url}/Users",
            query_params=query
        )
        resp = self.api_call(req)
        if resp.is_success():
            return Users.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def _ensure_user_id(self, id: str, user: User) -> str:
        if id:
            return id
        else:
            if user:
                return user.id
            else:
                raise SCIMError("User ID is missing for update_user call")

    def _to_user_dict(self, user: Union[dict, User]) -> dict:
        if user:
            user_dict: dict = user if isinstance(user, dict) else user.to_dict()
            user_dict["schemas"] = self.schema_values
            return user_dict
        else:
            return None

    # ----------------------------------------------
    # Group Management
    # ----------------------------------------------

    def create_group(
        self,
        group: Union[dict, Group]
    ) -> Group:
        """Creates a new group.

        https://api.slack.com/scim#groups

        :param user: if you give a dict value here, be noted that keys must be camel-cased,
            not your familiar snake-case style.
        """

        req = SCIMRequest(
            token=self.token,
            http_method="POST",
            url=f"{self.base_url}/Groups",
            json_body=self._to_group_dict(group),
        )
        resp = self.api_call(req)
        if resp.is_success():
            return Group.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def patch_group(
        self,
        id: str,
        group: Union[dict, Group]
    ) -> Group:
        """Partially updates a group.

        https://api.slack.com/scim#groups

        :param id: group ID
        :param user: if you give a dict value here, be noted that keys must be camel-cased,
            not your familiar snake-case style.
        """
        id = self._ensure_group_id(id, group)
        req = SCIMRequest(
            token=self.token,
            http_method="PATCH",
            url=f"{self.base_url}/Groups/{quote(id)}",
            json_body=self._to_group_dict(group),
        )
        resp = self.api_call(req)
        if resp.is_success():
            return Group.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def update_group(
        self,
        id: str,
        group: Union[dict, Group],
    ) -> Group:
        """Overwrites the whole group.

        https://api.slack.com/scim#groups

        :param id: group ID
        :param user: if you give a dict value here, be noted that keys must be camel-cased,
            not your familiar snake-case style.
        """
        id = self._ensure_group_id(id, group)
        req = SCIMRequest(
            token=self.token,
            http_method="PUT",
            url=f"{self.base_url}/Groups/{quote(id)}",
            json_body=self._to_group_dict(group),
        )
        resp = self.api_call(req)
        if resp.is_success():
            return Group.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def delete_group(
        self,
        id: str,
    ) -> Group:
        """Deletes a group.

        https://api.slack.com/scim#groups

        :param id: group ID
        """
        req = SCIMRequest(
            token=self.token,
            http_method="DELETE",
            url=f"{self.base_url}/Groups/{quote(id)}",
        )
        resp = self.api_call(req)
        if not resp.is_success():
            raise SCIMApiError.from_response(resp)

    def read_group(
        self,
        id: str,
    ) -> Group:
        """Finds a group by group ID.

        https://api.slack.com/scim#groups

        :param id: group ID
        """
        req = SCIMRequest(
            token=self.token,
            http_method="GET",
            url=f"{self.base_url}/Groups/{quote(id)}",
        )
        resp = self.api_call(req)
        if resp.is_success():
            return Group.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def search_groups(
        self,
        *,
        filter: str = None,
        count: int = None,
        start_index: int = None
    ) -> Groups:
        """Searches the groups matching the given filter.

        https://api.slack.com/scim#users

        :param filter: https://api.slack.com/scim#filter
        :param count: the number of results to return in a response
        :param start_index: the index to fetch as the first item
        """
        query = {}
        if filter:
            query["filter"] = filter
        if count:
            query["count"] = count
        if start_index:
            query["startIndex"] = start_index
        req = SCIMRequest(
            token=self.token,
            http_method="GET",
            url=f"{self.base_url}/Groups",
            query_params=query
        )
        resp = self.api_call(req)
        if resp.is_success():
            return Groups.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    def _ensure_group_id(self, id: str, group: Group) -> str:
        if id:
            return id
        else:
            if group:
                return group.id
            else:
                raise SCIMError("Group ID is missing for update_group call")

    def _to_group_dict(self, group: Union[dict, Group]) -> dict:
        if group:
            group_dict: dict = group if isinstance(group, dict) else group.to_dict()
            group_dict["schemas"] = self.schema_values
            return group_dict
        else:
            return None

    # ----------------------------------------------
    # ServiceProviderConfigs
    # ----------------------------------------------

    def get_service_provider_configs(self) -> ServiceProviderConfigs:
        """Fetches ServiceProviderConfigs"""
        req = SCIMRequest(
            token=self.token,
            http_method="GET",
            url=f"{self.base_url}/ServiceProviderConfigs",
        )
        resp = self.api_call(req)
        if resp.is_success():
            return ServiceProviderConfigs.from_dict(json.loads(resp.body)) if resp.body else None
        else:
            raise SCIMApiError.from_response(resp)

    # ----------------------------------------------
    # HTTP Client
    # ----------------------------------------------

    def api_call(self, api_request: SCIMRequest) -> SCIMResponse:
        """A general method to call the Slack SCIM APIs

        :param api_request: API request information
        :raise Exception: only when unexpected errors occur,
            never raises exceptions when getting an error code
            with unsuccessful HTTP status from Slack
        """
        http_method = api_request.http_method.upper()
        url = api_request.url
        if api_request.query_params:
            params = copy.copy(api_request.query_params)
            if http_method == "GET" and api_request.body_params:
                params.update(api_request.body_params)
            q = urlencode(params)
            url = url + (f"&{q}" if "?" in url else f"?{q}")
            pass

        headers = copy.copy(api_request.headers)
        headers["Authorization"] = f"Bearer {api_request.token}"
        if api_request.json_body:
            body: dict = self._to_non_null_dict(copy.copy(api_request.json_body))
            req_body: str = None if http_method == "GET" \
                else json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json;charset=utf-8"
        else:
            req_body: str = None if http_method == "GET" \
                else urlencode(api_request.body_params).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded;charset=utf-8"

        try:
            http_request: Request = Request(
                method=http_method,
                url=url,
                data=req_body,
                headers=headers
            )
            self._debug_log_request(http_request, req_body)

            http_response: HTTPResponse = urlopen(http_request)
            charset: str = http_response.headers.get_content_charset()
            raw_body: bytes = http_response.read()
            resp_body: str = raw_body.decode(charset) if raw_body else None

            api_response = SCIMResponse(
                status=http_response.status,
                reason=http_response.reason,
                headers=http_response.headers,
                body=resp_body,
            )
            self._debug_log_completion(http_request, api_response)
            return api_response

        except HTTPError as e:
            # TODO: rate limit
            api_response = SCIMResponse(
                status=e.code,
                reason=e.reason,
                headers=e.headers,
                body=e.read().decode("utf-8"),
            )
            self._debug_log_completion(http_request, api_response)
            return api_response
        except Exception as e:
            self._logger.error(f"Failed to send a request to Slack SCIM API server: {e}")
            raise e

    def _to_non_null_dict(self, d: Union[dict, any]) -> dict:
        """Recursively converts an object to dict"""
        result = {}
        if isinstance(d, dict):
            for key, value in d.items():
                if value is None:
                    continue
                if isinstance(value, dict):
                    value = self._to_non_null_dict(value)
                    result[key] = value
                elif isinstance(value, list):
                    new_list = []
                    for v in value:
                        v = self._to_non_null_dict(v)
                        if v:
                            new_list.append(v)
                    result[key] = new_list
                else:
                    result[key] = value
            return result
        elif getattr(d, "to_dict", None):
            return d.to_dict()
        else:
            return d

    def _debug_log_request(self, req: Request, body: str):
        if self._logger.level <= logging.DEBUG:
            headers_part = "\n".join([
                f"{k}: (redacted)" if k.lower() == "authorization" else f"{k}: {v}"
                for k, v in req.headers.items()
            ])
            message = f"*** SCIM API Request ***\n" \
                      f"{req.method} {req.full_url}\n" \
                      f"{headers_part}\n\n" \
                      f"{body or ''}\n"
            self._logger.debug(message)

    def _debug_log_completion(self, req: Request, resp: SCIMResponse):
        if self._logger.level <= logging.DEBUG:
            headers_part = "\n".join([f"{k}: {v}" for k, v in resp.headers.items()])
            message = f"*** SCIM API Response ***\n" \
                      f"{req.method} {req.full_url}\n" \
                      f"{resp.status} {resp.reason}\n" \
                      f"{headers_part}\n\n" \
                      f"{resp.body or ''}\n"
            self._logger.debug(message)
