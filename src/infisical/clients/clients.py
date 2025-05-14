"""Infisical SDK HTTPX clients.

# Available Resource APIs for the Clients:

- [Secrets][src.infisical.resources.secrets.api.]
- [Folders][src.infisical.resources.folders.api.]
- [Certificates][src.infisical.resources.certificates.api.]
"""

import json
from collections.abc import Callable, Coroutine
from typing import Any, Literal, Self, Unpack

import httpx
from pydantic import BaseModel

from infisical._types import InfisicalClientParams
from infisical.clients.base import BaseClient


class InfisicalClient(BaseClient):
    """Synchronous Client.

    Attributes:
        client (httpx.Client): The HTTPX client used for making requests.
    """

    def __init__(self, **kwargs: Unpack[InfisicalClientParams]) -> None:
        """Initialize with any [client parameter][src.infisical._types.InfisicalClientParams]."""
        super().__init__(**kwargs)
        self.client = httpx.Client(verify=self._verify_ssl, follow_redirects=self._follow_redirects)

    def __enter__(self) -> Self:
        """Enter the context manager and return this class.

        Returns:
            (Self): The current instance of the class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        """Exit the context manager and close the HTTPX client.

        !!! note

            While the stack trace is not used, it is required by the context manager protocol.
        """
        self.close()

    def close(self) -> None:
        """Close the HTTPX client."""
        self.client.close()

    def create_request(
        self,
        method: Literal["get", "post", "put", "delete", "patch"],
        url: str,
        params: dict | None = None,
        body: dict | None = None,
    ) -> Callable:
        """Create an anonymous function that encapsulates the request for the resource.

        This method generates a request for the resource using the HTTPX client. It is similar to the
        [`create_request`][(m).InfisicalAsyncClient.] method in the [InfisicalAsyncClient][(m).] class,
        but it returns a callable that will be called by the [`handle_request`][(c).] method.

        Args:
            method (Literal["get", "post", "put", "delete", "patch"]): The HTTPX client method name as a string
                to use for the request.
            url (str): The URL to send the request to.
            params (dict | None, optional): The query parameters to include in the request. Defaults to None.
            body (dict | None, optional): The body of the request. Defaults to None.
        """
        self.logger.debug(
            "Creating sync request for url %s with method %s params %s and body %s",
            url,
            method,
            params,
            body,
        )
        if method == "delete":
            # httpx does not support passing a body with DELETE requests, so we have to use the request method
            # instead. For further details, see https://lists.w3.org/Archives/Public/ietf-http-wg/2020JanMar/0123.html
            return lambda: self.client.request(
                method="DELETE",
                url=url,
                headers=self.__get_headers__(method),
                content=json.dumps(body).encode("utf-8"),
            )
        # Get the method from the client
        _call = getattr(self.client, method)
        # Create common kwargs for the call
        call_kwargs = {"url": url, "headers": self.__get_headers__(method), "params": params}
        if method == "get":
            # GET requests don't have a body, so we don't need to pass it
            return lambda: _call(**call_kwargs)
        # For all other requests, we pass the body
        call_kwargs["json"] = body
        return lambda: _call(**call_kwargs)

    def handle_request(
        self,
        request: Callable,
        expected_responses: dict[str, BaseModel] | None = None,
    ) -> BaseModel | Any:  # noqa: ANN401
        """Handle the synchronous HTTP request.

        This method is similar to the [`handle_request`][(m).InfisicalAsyncClient.] method in the
        [InfisicalAsyncClient][(m).] class, but it calls the anonymous synchronous function created in the
        [`create_request`][(c).]. method.

        The `expected_responses` parameter is typically a dictionary containing a mapping of possible keys within the
        response JSON to look for and the corresponding model to validate against. If None, the entire response JSON
        will be returned, which could be `Any` type. If the key is an empty string, it will validate the entire
        response JSON against the model. If none of the keys are found in the response JSON, it will raise a
        `ValueError`.

        Args:
            request (Callable): The callable to call.
            expected_responses (dict[str, BaseModel] | None): The expected responses for the request.
        """
        response = request()
        return self.__handle_response__(response=response, expected_responses=expected_responses)


class InfisicalAsyncClient(BaseClient):
    """Asynchronous Client.

    Attributes:
        client (httpx.AsyncClient): The HTTPX async client used for making requests.
    """

    def __init__(self, **kwargs: Unpack[InfisicalClientParams]) -> None:
        """Initialize with any [client parameter][src.infisical._types.InfisicalClientParams]."""
        super().__init__(**kwargs)
        self.client = httpx.AsyncClient(verify=self._verify_ssl, follow_redirects=self._follow_redirects)

    async def __aenter__(self) -> Self:
        """Enter the `async` context manager and return class.

        Returns:
            (Self): The current instance of the class.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        """Exit the context manager and close the HTTPX async client.

        !!! note
            While the stack trace is not used, it is required by the context manager protocol.
        """
        await self.close()

    async def close(self) -> None:
        """Close the HTTPX async client."""
        await self.client.aclose()

    def create_request(
        self,
        method: Literal["get", "post", "put", "delete", "patch"],
        url: str,
        params: dict | None = None,
        body: dict | None = None,
    ) -> Coroutine:
        """Create a Coroutine request for the resource to be awaited.

        This method generates a request for the resource using the HTTPX `AsyncClient`. It is similar to the
        [`create_request`][(m).InfisicalClient.] method in the [InfisicalClient][(m).] class, but it returns a
        coroutine that will be awaited by the [`handle_request`][(c).] method.

        Args:
            method (Literal["get", "post", "put", "delete", "patch"]): The HTTPX client method name as a string
                to use for the request.
            url (str): The URL to send the request to.
            params (dict | None, optional): The query parameters to include in the request. Defaults to None.
            body (dict | None, optional): The body of the request. Defaults to None.
        """
        self.logger.debug(
            "Creating async request for url %s with method %s params %s and body %s",
            url,
            method,
            params,
            body,
        )
        if method == "delete":
            # httpx does not support passing a body with DELETE requests, so we have to use the request method
            # instead. For further details, see https://lists.w3.org/Archives/Public/ietf-http-wg/2020JanMar/0123.html
            return self.client.request(
                method="DELETE",
                url=url,
                headers=self.__get_headers__(method),
                content=json.dumps(body).encode("utf-8") if body else None,
            )
        if method == "get":
            # GET requests don't have a body, so we don't need to pass it
            return getattr(self.client, method)(url, params=params, headers=self.__get_headers__(method))
        # For all other requests, we pass the body
        return getattr(self.client, method)(url, params=params, json=body, headers=self.__get_headers__(method))

    async def handle_request(
        self,
        *,
        request: Coroutine,
        expected_responses: dict[str, BaseModel] | None = None,
    ) -> BaseModel | Any:  # noqa: ANN401
        """Handle the asynchronous request.

        This method is similar to the [`handle_request`][(m).InfisicalClient.] method in the [InfisicalClient][(m).],
        but it `await`'s the coroutine returned by the [`create_request`][(c).] method.

        The `expected_responses` parameter is typically a dictionary containing a mapping of possible keys within the
        response JSON to look for and the corresponding model to validate against. If None, the entire response JSON
        will be returned, which could be `Any` type. If the key is an empty string, it will validate the entire
        response JSON against the model. If none of the keys are found in the response JSON, it will raise a
        `ValueError`.

        Args:
            request (Coroutine): The coroutine to await.
            expected_responses (dict[str, BaseModel] | None): The expected responses for the request.
        """
        response = await request
        return self.__handle_response__(response=response, expected_responses=expected_responses)
