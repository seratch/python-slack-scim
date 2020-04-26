import json
from typing import Dict

from .response import SCIMResponse


class SCIMError(Exception):
    def __init__(self, errors: Dict[str, any]):
        """Represents a general error in this library

        :param errors: Specific error information
        """
        super()
        self.errors = errors

    def to_dict(self) -> dict:
        result: dict = {}
        result["errors"] = self.errors
        return result

    def __repr__(self):
        return f"<slack_scim.{self.__class__.__name__}: {self.to_dict()}>"


class SCIMApiError(SCIMError):
    def __init__(
        self,
        *,
        status: int,
        headers: Dict[str, str],
        errors: Dict[str, any],
    ):
        """Exception representing an error returned by Slack

        :param status: HTTP status code
        :param headers: All the response headers
        :param errors: Error messages returned by Slack
        """
        super(SCIMApiError, self).__init__(errors)
        self.status = status
        self.headers = headers
        self.errors = errors

    @classmethod
    def from_response(cls, resp: SCIMResponse) -> "SCIMApiError":
        errors = {}
        if resp.body:
            b = json.loads(resp.body)
            errors = b["Errors"] if "Errors" in b else {}
        return SCIMApiError(
            status=resp.status,
            headers=resp.headers,
            errors=errors,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = self.status
        result["headers"] = self.headers
        result["errors"] = self.errors
        return result

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return f"<slack_scim.{self.__class__.__name__}: {self.to_dict()}>"
