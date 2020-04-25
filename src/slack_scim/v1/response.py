from typing import Dict


class SCIMResponse():
    def __init__(
        self,
        *,
        status: int,
        reason: str,
        headers: Dict[str, str],
        body: str,
    ):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body

    def is_success(self) -> bool:
        return self.status < 300

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = self.status
        result["reason"] = self.reason
        result["headers"] = self.headers
        result["body"] = self.body
        return result

    def __str__(self):
        return str(self.to_dict())
