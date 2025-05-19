from importlib import reload
from collections.abc import Callable, Coroutine
import ssl
from unittest.mock import MagicMock, patch, AsyncMock
import httpx
from pydantic import BaseModel
import pytest

import infisical
from infisical.clients import InfisicalClient, InfisicalAsyncClient
from infisical.clients.base import BaseClient
from infisical.exceptions import InfisicalHTTPError
from infisical.resources.certificates.api import Certificates
from infisical.resources.folders.api import Folders
from infisical.resources.secrets.api import Secrets

class MockResponse(BaseModel):
    val: str


class TestClientsCommon:
    @pytest.mark.parametrize("follow_redirects", [True, False])
    @pytest.mark.parametrize("client,httpx_client", [(InfisicalClient, httpx.Client), (InfisicalAsyncClient, httpx.AsyncClient)])
    @patch(f"{BaseClient.__module__}.InfisicalCredentialProviderChain")
    def test_clients_init(self, mock_chain, client, httpx_client, follow_redirects):
        mock_credentials = mock_chain.return_value.resolve.return_value
        mock_credentials.url = "https://test.example"
        test_client = client(follow_redirects=follow_redirects)
        # Check init settings
        assert isinstance(test_client.client, httpx_client)
        assert test_client.client.follow_redirects == follow_redirects
        assert test_client.url == "https://test.example"
        mock_chain.return_value.resolve.assert_called_once()
        # Check APIs
        assert isinstance(test_client.certificates, Certificates)
        assert isinstance(test_client.folders, Folders)
        assert isinstance(test_client.secrets, Secrets)

    @pytest.mark.parametrize("client", [InfisicalClient, InfisicalAsyncClient])
    @pytest.mark.parametrize("method", ["get", "post", "put", "delete", "patch"])
    @patch(f"{BaseClient.__module__}.InfisicalCredentialProviderChain")
    def test_clients_headers(self, mock_chain, client, method):
        mock_credentials = mock_chain.return_value.resolve.return_value
        mock_credentials.get_token.return_value = "test_token"

        test_client: BaseClient = client()
        # Check headers
        expected_headers = {
            "Authorization": "Bearer test_token",
            "Accept": "application/json",
        }
        if method != "get":
            expected_headers["Content-Type"] = "application/json"
        assert test_client.__get_headers__(method) == expected_headers

    @pytest.mark.parametrize("method", ["get", "post", "put", "delete", "patch"])
    @pytest.mark.parametrize("client", [InfisicalClient, InfisicalAsyncClient])
    @patch(f"{BaseClient.__module__}.InfisicalCredentialProviderChain")
    def test_create_request(self, _, client, method):
        test_client: BaseClient = client()
        expected = Callable if isinstance(test_client.client, httpx.Client) else Coroutine
        result = test_client.create_request(method=method, url="https://test.example", params={"foo": "bar"}, body={"foo": "bar"})
        assert isinstance(result, expected)

    @pytest.mark.parametrize("status_code,json,expected_responses,expected", [
        (400, {"message": "test", "statusCode": 400, "details": "detail"}, {}, InfisicalHTTPError),
        (500, {"message": "test", "statusCode": 500}, {}, InfisicalHTTPError),
        (200, {"foo": "bar"}, {"bad": MockResponse}, ValueError),
        (200, "blah", {}, "blah"),
        (200, {"val": "test"}, {"": MockResponse}, MockResponse(val="test")),
        (200, {"nested": {"val": "test"}}, {"nested": MockResponse}, MockResponse(val="test")),
    ])
    @pytest.mark.parametrize("client", [InfisicalClient, InfisicalAsyncClient])
    @patch(f"{BaseClient.__module__}.InfisicalCredentialProviderChain")
    def test_handle_response(self, _, client, status_code, json, expected_responses, expected, mock_response):
        test_client: BaseClient = client()
        response: httpx.Response = mock_response(status_code=status_code, json=json)

        if isinstance(expected, type(Exception)):
            with pytest.raises(expected):
                test_client.__handle_response__(response=response, expected_responses=expected_responses)
        else:
            assert test_client.__handle_response__(response=response, expected_responses=expected_responses) == expected


class TestInfisicalClient:
    @pytest.mark.parametrize("method", ["get", "post", "put", "delete", "patch"])
    @patch(f"{InfisicalClient.__module__}.httpx")
    @patch(f"{BaseClient.__module__}.InfisicalCredentialProviderChain")
    def test_handle_request(self, _, mock_httpx, method, mock_request):
        mock_handle_response = MagicMock()
        
        match method:
            case "get":
                mock_httpx.Client.return_value.get = mock_request.call
            case "post":
                mock_httpx.Client.return_value.post = mock_request.call
            case "put":
                mock_httpx.Client.return_value.put = mock_request.call
            case "delete":
                mock_httpx.Client.return_value.request = mock_request.call
            case "patch":
                mock_httpx.Client.return_value.patch = mock_request.call
            case _:
                raise ValueError(f"Invalid method: {method}")

        with InfisicalClient() as client:
            client.__handle_response__ = mock_handle_response
            test_request = client.create_request(method=method, url="https://test.example", params={"foo": "bar"}, body={"foo": "bar"})
            client.handle_request(request=test_request, expected_responses={})
        
        assert mock_request.called
        mock_handle_response.assert_called_once_with(
            response=mock_request.response,
            expected_responses={},
        )


@pytest.mark.asyncio(loop_scope="class")
class TestInfisicalAsyncClient:
    @pytest.mark.parametrize("method", ["get", "post", "put", "delete", "patch"])
    @patch(f"{InfisicalAsyncClient.__module__}.httpx")
    @patch(f"{BaseClient.__module__}.InfisicalCredentialProviderChain")
    async def test_handle_request(self, _, mock_httpx, method):
        mock_handle_response = MagicMock()
        mock_httpx.AsyncClient.return_value.aclose = AsyncMock()

        mock_response = "mock_response"

        match method:
            case "get":
                mock_httpx.AsyncClient.return_value.get = AsyncMock(return_value=mock_response)
            case "post":
                mock_httpx.AsyncClient.return_value.post = AsyncMock(return_value=mock_response)
            case "put":
                mock_httpx.AsyncClient.return_value.put = AsyncMock(return_value=mock_response)
            case "delete":
                mock_httpx.AsyncClient.return_value.request = AsyncMock(return_value=mock_response)
            case "patch":
                mock_httpx.AsyncClient.return_value.patch = AsyncMock(return_value=mock_response)
            case _:
                raise ValueError(f"Invalid method: {method}")

        async with InfisicalAsyncClient() as client:
            client.__handle_response__ = mock_handle_response
            test_request = client.create_request(method=method, url="https://test.example", params={"foo": "bar"}, body={"foo": "bar"})
            await client.handle_request(request=test_request, expected_responses={})
        
        mock_handle_response.assert_called_once_with(
            response=mock_response,
            expected_responses={},
        )
