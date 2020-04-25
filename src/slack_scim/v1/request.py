from typing import Dict


class SCIMRequest():
    def __init__(
        self,
        *,
        token: str,
        http_method: str,
        url: str,
        query_params: Dict[str, str] = dict(),
        body_params: Dict[str, str] = dict(),
        json_body: Dict = dict(),
        headers: Dict[str, str] = dict(),
    ):
        self.token = token
        self.http_method = http_method
        self.url = url
        self.headers = headers
        self.query_params = query_params
        self.body_params = body_params
        self.json_body = json_body

    def to_dict(self) -> dict:
        result: dict = {"token": "redacted"}
        result["http_method"] = self.http_method
        result["url"] = self.url
        result["headers"] = self.headers
        result["query_params"] = self.query_params
        result["body_params"] = self.body_params
        result["json_body"] = self.json_body
        return result

    def __str__(self):
        return str(self.to_dict())
