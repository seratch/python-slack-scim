import unittest

from slack_scim import SCIMClient
from tests.v1 import load_token
from tests.v1.mock_server import setup_mock_server, cleanup_mock_server


class TestServiceProviderConfigs(unittest.TestCase):
    def setUp(self):
        setup_mock_server(self)
        # `admin` scope required
        self.token = load_token()
        base_url = self.server_url or SCIMClient.production_base_url
        self.client = SCIMClient(token=self.token, base_url=base_url)

    def tearDown(self):
        cleanup_mock_server(self)

    def test_call(self):
        result = self.client.get_service_provider_configs()
        assert result is not None
        assert len(result.authentication_schemes) > 0
