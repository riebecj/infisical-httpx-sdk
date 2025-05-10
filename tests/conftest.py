import json
import time
from typing import Literal
from unittest.mock import MagicMock
import httpx
import pytest

from jwcrypto.jwe import JWE
from jwcrypto.jwt import JWT
from jwcrypto.jwk import JWK

from infisical.resources.base import InfisicalAPI

TEST_ENDPOINT = "https://test.example"

@pytest.fixture
def generate_jwe():
    def _generate_jwe(passphrase: str, payload: dict) -> str:
        jwe = JWE(
            plaintext=json.dumps(json.dumps(payload)).encode(),  # Double-wrap the payload, as that's what Infisical does
            protected=json.dumps({
                "alg":"PBES2-HS256+A128KW",
                "enc":"A256GCM",
            }),
        )
        jwe.add_recipient(passphrase.encode())
        return jwe.serialize(compact=True)
    return _generate_jwe


@pytest.fixture
def generate_jwt():
    def _generate_jwt(status: Literal["valid", "invalid", "expired"] = "valid") -> str:
        if status == "invalid":
            claims = {"iat": time.time() + 9000, "exp": 0}
        elif status == "expired":
            claims = {"iat": 0, "exp": 0}
        else:
            claims = {"iat": time.time(), "exp": time.time() + 9000}
        key = JWK(generate='oct', size=256)
        token = JWT(header={"alg": "HS256"}, claims=claims)
        token.make_signed_token(key)
        return token.serialize(compact=True)
    return _generate_jwt


@pytest.fixture
def format_url():
    def _format_url(api: InfisicalAPI, uri: str) -> str:
        return f"{TEST_ENDPOINT}/api/{api.base_uri.strip('/')}/{uri.strip('/')}"
    return _format_url


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.url = TEST_ENDPOINT
    return client


@pytest.fixture
def mock_response():
    def _mock_response(status_code: int, json: dict = None):
        return httpx.Response(
            status_code=status_code,
            request=httpx.Request(method="get", url="https://test/example"),
            json=json
        )
    return _mock_response


@pytest.fixture
def mock_request():
    class MockRequest:
        def __init__(self):
            self.called = False
            self.response = "blah"
        
        def call(self, *args, **kwargs):
            self.called = True
            return self.response
    return MockRequest()


def mock_async_response():
    class MockAsyncResponse:
        def __init__(self, status_code: int, json: dict = None):
            self.status_code = status_code
            self.json_data = json

        async def json(self):
            return self.json_data

    return MockAsyncResponse
