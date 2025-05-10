"""Infisical SDk HTTPX clients."""

import logging
import os
from abc import abstractmethod
from collections.abc import Callable, Coroutine
from typing import Any, Literal, Unpack

import httpx
from pydantic import BaseModel

from infisical._types import InfisicalClientParams
from infisical.credentials.providers import InfisicalCredentialProviderChain
from infisical.exceptions import InfisicalHTTPError
from infisical.resources.certificates.api import Certificates
from infisical.resources.folders.api import Folders
from infisical.resources.secrets.api import Secrets

HttpxMethod = Literal["get", "post", "put", "delete", "patch"]


class BaseClient:
    """Infisical SDK Base Client.

    This is the base class for both the synchronous and asynchronous clients. It handles the common functionality
    between the two clients, such as creating requests, handling responses, and managing the credentials.
    It is not meant to be used directly, but rather as a base class for the `InfisicalClient` and `InfisicalAsyncClient`
    classes.
    """

    # These are not a true class properties, but rather a placeholders to satisfy the type checker and provide a
    # consistent interface for the clients. The properties are set in the `__set_apis__` method.
    client: httpx.Client | httpx.AsyncClient
    certificates: Certificates
    folders: Folders
    secrets: Secrets

    def __init__(self, **kwargs: Unpack[InfisicalClientParams]) -> None:
        """Initialize the Infisical Client."""
        self._verify_ssl = kwargs.pop("verify_ssl", True)
        self._follow_redirects = kwargs.pop("follow_redirects", False)
        os.environ["INFISICAL_VERIFY_SSL"] = str(self._verify_ssl)  # Set it for the provider chain
        self._credentials = kwargs.pop("provider_chain", InfisicalCredentialProviderChain(**kwargs)).resolve()
        self.url = self._credentials.url
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__set_apis__()

    def __set_apis__(self) -> None:
        """Set the APIs in a separate dunder method to keep the constructor clean."""
        self.logger.debug("Setting up APIs")
        self.certificates = Certificates(self)
        self.folders = Folders(self)
        self.secrets = Secrets(self)

    def _get_headers(self, method: HttpxMethod) -> dict:
        """Generate the headers for the request.

        The headers will include the `Authorization` header with the bearer token and the `Content-Type` header if
        the method is not a GET request. The `Authorization` header will be set to the token from the credentials
        acquired from the `InfisicalCredentialProviderChain`. We call `get_token()` every time to ensure we get a
        valid token, as there is refresh logic in the credential object to handle token expiration.

        NOTE: Token refreshing only happens if the credentials acquired are Universal Auth credentials (Client ID and
        Secret). If the credentials are not Universal Auth credentials, the token cannot be refreshed and expiration
        will raise an exception.
        """
        self.logger.debug("Generating headers for request method: %s", method)
        headers = {"Authorization": f"Bearer {self._credentials.get_token()}", "Accept": "application/json"}
        if method != "get":
            headers["Content-Type"] = "application/json"
        return headers

    @abstractmethod
    def create_request(
        self,
        method: HttpxMethod,
        url: str,
        params: dict | None = None,
        body: dict | None = None,
    ) -> Callable | Coroutine:
        """Abstract method to create a request for the resource."""
        msg = "This method should be implemented in the subclass."
        raise NotImplementedError(msg)

    def _handle_response(
        self,
        response: httpx.Response,
        expected_responses: dict[str, BaseModel] | None = None,
    ) -> BaseModel | Any:  # noqa: ANN401
        """Handle the response from the request.

        The response object will raise an exception if the status code is not 2xx. If the status code is 4xx or 5xx,
        it will raise an `InfisicalHTTPError` stacked with the `httpx.HTTPStatusError`. We will parse error response
        JSON to provide more context about the error.

        If the status code is 2xx, it will validate the response JSON against the expected responses, which is a dict
        of response JSON keys to their corresponding models. If the key is an empty string, it will validate the
        entire response JSON against the model. If none of the keys are found in the response JSON, it will raise a
        `ValueError`.

        Args:
            response (httpx.Response): The response object from the request.
            expected_responses (dict[str, BaseModel]): A dict of response JSON keys to their corresponding models.

        Returns:
            BaseModel: The validated response model.
            Any: The raw response JSON if no expected responses are provided.
        """
        self.logger.debug("Handling response with status code %s", response.status_code)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            self.logger.exception("HTTP Error")
            raise InfisicalHTTPError(response.json()) from exc
        else:
            self.logger.debug("Parsing response with expectations: %s", expected_responses)
            data = response.json()
            self.logger.debug("Response data: %s", data)
            if not expected_responses:
                self.logger.debug("No response expectations provided, returning raw response data")
                return data
            for key, model in expected_responses.items():
                if not key:
                    return model.model_validate(data)
                if key and key in data:
                    return model.model_validate(data[key])
            self.logger.debug("Response expectations %s not found in response data: %s", expected_responses, data)
            msg = f"None of the keys {expected_responses.keys()} were found in the response data."
            raise ValueError(msg)
