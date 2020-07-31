import json
import logging
import threading
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Type
from unittest import TestCase
from urllib.parse import urlparse

from tests.v1 import is_prod_test_mode


class MockHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    default_request_version = "HTTP/1.1"
    logger = logging.getLogger(__name__)

    def is_valid_token(self):
        return "authorization" in self.headers \
               and str(self.headers["authorization"]).startswith("Bearer xoxp-")

    def set_common_headers(self):
        self.send_header("content-type", "application/json;charset=utf-8")
        self.send_header("connection", "close")
        self.end_headers()

    def do_GET(self):
        if self.is_valid_token():
            parsed_path = urlparse(self.path)
            if parsed_path.path == "/ServiceProviderConfigs":
                with open("tests/fixture/v1_service_provider_configs.json") as f:
                    body = f.read()
            elif parsed_path.path == "/Users":
                if "startIndex=2" in parsed_path.query:
                    with open("tests/fixture/v1_users_2.json") as f:
                        body = f.read()
                else:
                    with open("tests/fixture/v1_users_1.json") as f:
                        body = f.read()
            elif parsed_path.path == "/Users/W111":
                with open("tests/fixture/v1_user_1.json") as f:
                    body = f.read()
            elif parsed_path.path == "/Users/W222":
                with open("tests/fixture/v1_user_2.json") as f:
                    body = f.read()
            elif parsed_path.path == "/Groups":
                if "startIndex=2" in parsed_path.query:
                    with open("tests/fixture/v1_groups_2.json") as f:
                        body = f.read()
                else:
                    with open("tests/fixture/v1_groups_1.json") as f:
                        body = f.read()
            elif parsed_path.path == "/Groups/S111":
                with open("tests/fixture/v1_group_1.json") as f:
                    body = f.read()
            elif parsed_path.path == "/Groups/S222":
                with open("tests/fixture/v1_group_2.json") as f:
                    body = f.read()
            elif parsed_path.path == "/Groups/S333":
                with open("tests/fixture/v1_group_3.json") as f:
                    body = f.read()
            else:
                body = "{}"
            self.send_response(HTTPStatus.OK)
            self.set_common_headers()
            self.wfile.write(body.encode("utf-8"))
            self.wfile.close()
        else:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.set_common_headers()


    def do_POST(self):
        if self.is_valid_token():
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            input = json.loads(post_body)

            parsed_path = urlparse(self.path)
            if parsed_path.path == "/Users":
                with open("tests/fixture/v1_user_1.json") as f:
                    body = f.read()
                    b = json.loads(body)
                    b["id"] = "W111"
                    b["emails"] = input["emails"]
                    b["name"] = input["name"]
                    b["userName"] = input["userName"]
                    body = json.dumps(b)
            elif parsed_path.path == "/Groups":
                with open("tests/fixture/v1_group_1.json") as f:
                    body = f.read()
                    b = json.loads(body)
                    b["id"] = "S111"
                    if "displayName" in input:
                        b["displayName"] = input["displayName"]
                    if "members" in input:
                        b["members"] = input["members"]
                    body = json.dumps(b)
            else:
                body = "{}"
            self.send_response(HTTPStatus.OK)
            self.set_common_headers()
            self.wfile.write(body.encode("utf-8"))
            self.wfile.close()
        else:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.set_common_headers()

    def do_PATCH(self):
        if self.is_valid_token():
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            input = json.loads(post_body)

            parsed_path = urlparse(self.path)
            if parsed_path.path == "/Users/W111":
                with open("tests/fixture/v1_user_1.json") as f:
                    body = f.read()
                    b = json.loads(body)
                    b["id"] = "W111"
                    if "emails" in input:
                        b["emails"] = input["emails"]
                    if "name" in input:
                        b["name"] = input["name"]
                    if "userName" in input:
                        b["userName"] = input["userName"]
                    body = json.dumps(b)
            elif parsed_path.path == "/Groups/S111":
                with open("tests/fixture/v1_group_1.json") as f:
                    body = f.read()
                    b = json.loads(body)
                    b["id"] = "S111"
                    if "displayName" in input:
                        b["displayName"] = input["displayName"]
                    if "members" in input:
                        b["members"] = input["members"]
                    body = json.dumps(b)
            else:
                body = "{}"
            print(body)
            self.send_response(HTTPStatus.OK)
            self.set_common_headers()
            self.wfile.write(body.encode("utf-8"))
            self.wfile.close()
        else:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.set_common_headers()

    def do_PUT(self):
        if self.is_valid_token():
            parsed_path = urlparse(self.path)
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            input = json.loads(post_body)

            if parsed_path.path == "/Users/W111":
                with open("tests/fixture/v1_user_1.json") as f:
                    body = f.read()
                    b = json.loads(body)
                    b["id"] = "W111"
                    if "emails" in input:
                        b["emails"] = input["emails"]
                    if "name" in input:
                        b["name"] = input["name"]
                    if "userName" in input:
                        b["userName"] = input["userName"]
                    body = json.dumps(b)
            elif parsed_path.path == "/Groups/S111":
                with open("tests/fixture/v1_group_1.json") as f:
                    body = f.read()
                    b = json.loads(body)
                    b["id"] = "S111"
                    if "displayName" in input:
                        b["displayName"] = input["displayName"]
                    if "members" in input:
                        b["members"] = input["members"]
                    body = json.dumps(b)
            else:
                body = "{}"
            self.send_response(HTTPStatus.OK)
            self.set_common_headers()
            self.wfile.write(body.encode("utf-8"))
            self.wfile.close()
        else:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.set_common_headers()

    def do_DELETE(self):
        if self.is_valid_token():
            self.send_response(HTTPStatus.OK)
            self.set_common_headers()
        else:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.set_common_headers()


class MockServerThread(threading.Thread):

    def __init__(self, test: TestCase, handler: Type[SimpleHTTPRequestHandler] = MockHandler):
        threading.Thread.__init__(self)
        self.handler = handler
        self.test = test

    def run(self):
        self.server = HTTPServer(('localhost', 8888), self.handler)
        self.test.server_url = "http://localhost:8888"
        self.test.host, self.test.port = self.server.socket.getsockname()
        self.test.server_started.set()  # threading.Event()

        self.test = None
        try:
            self.server.serve_forever(0.05)
        finally:
            self.server.server_close()

    def stop(self):
        self.server.shutdown()
        self.join()


def setup_mock_server(test: TestCase):
    if is_prod_test_mode():
        test.server_url = None
    else:
        test.server_started = threading.Event()
        test.thread = MockServerThread(test)
        test.thread.start()
        test.server_started.wait()


def cleanup_mock_server(test: TestCase):
    if not is_prod_test_mode():
        test.thread.stop()
        test.thread = None
