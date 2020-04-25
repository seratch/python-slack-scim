import json
from typing import Dict

from .response import SCIMResponse


class SCIMError(Exception):
    def __init__(self, errors: Dict[str, any]):
        super()
        self.errors = errors


class SCIMApiError(SCIMError):
    def __init__(
        self,
        *,
        status: int,
        headers: Dict[str, str],
        errors: Dict[str, any],
    ):
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
