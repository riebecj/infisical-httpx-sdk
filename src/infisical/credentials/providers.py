"""Infisical Credential Providers."""

import json
import os
import time
from abc import ABC, abstractmethod

import httpx
from jwcrypto.jwt import JWT, JWTExpired, JWTNotYetValid

from infisical.credentials.keyring_handler import FileKeyringBackend


class InfisicalCredentialsError(Exception):
    """Base class for Infisical credentials errors."""


class InfisicalCredentials:
    """Represents Infisical credentials.

    This can be initialized with a token, in which case it is ineligible for refresh.
    If `client_id` and `client_secret` are provided, it can be refreshed by calling the auth endpoint
    again with the client ID and secret.

    An explicit `url` or provider-based `url` will always be preferred. If none is provided, it will default to
    checking the `INFISICAL_URL` environment variable, ultimately defaulting to "https://us.infisical.com" if not set.
    """

    def __init__(self, url: str, token: str, client_id: str, client_secret: str) -> None:
        """Initialize the class.

        Args:
            url (str): The base URL for the Infisical API.
            token (str): The JWT token for authentication.
            client_id (str, optional): The client ID for refreshing the token.
            client_secret (str, optional): The client secret for refreshing the token.
        """
        self.url = url.rstrip("/")  # Just in case the user passes a URL with a trailing slash that isn't caught.
        self._token = token
        self._client_id = client_id
        self._client_secret = client_secret
        self._refreshable = False
        if self._client_id and self._client_secret:
            # If client_id and client_secret are provided, we can refresh by calling the auth endpoint.
            self._refreshable = True

    def is_valid(self) -> bool:
        """Check if the credentials are valid."""
        return bool(self._token)

    def get_token(self) -> str:
        """Get the JWT token."""
        self._check_refresh()
        return self._token

    def refreshable(self) -> bool:
        """Check if the credentials are refreshable."""
        return self._refreshable

    def refresh(self) -> None:
        """Refresh the credentials by calling the Infisical auth endpoint.

        This method will only work if the credentials are refreshable, i.e., if `client_id` and `client_secret` are
        provided. If the credentials are not refreshable, this method will do nothing.
        """
        if not self._refreshable:
            return

        verify = os.getenv("INFISICAL_VERIFY_SSL", "true").lower() not in ("0", "false", "no")
        with httpx.Client(verify=verify) as client:
            response = client.post(
                f"{self.url}/api/v1/auth/universal-auth/login",
                json={
                    "clientId": self._client_id,
                    "clientSecret": self._client_secret,
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            response.raise_for_status()
            self._token = response.json()["accessToken"]

    def _check_refresh(self) -> None:
        """Check if the credentials are expired, and refreshes them if available.

        The token is either explicitly set by the provider, or it is set by the `refresh()` method called by the
        provider. If the token is expired and refreshable, it will be refreshed. If it is not refreshable, an error will
        be raised.
        """
        if not self._token:
            return
        jwt = JWT(jwt=self._token)
        payload = json.loads(jwt.token.objects["payload"].decode())
        try:
            # Check if the token is not expired and has a valid issued at time.
            # Rather than checking if claims are present, assume 0. This will raise an expiration error.
            jwt._check_nbf(payload["iat"], time.time(), 0)  # noqa: SLF001
            jwt._check_exp(payload["exp"], time.time(), 0)  # noqa: SLF001
        except JWTExpired as exc:
            if self._refreshable:
                self.refresh()
            else:
                msg = "The credentials have expired."
                raise InfisicalCredentialsError(msg) from exc
        except JWTNotYetValid as exc:
            msg = "The provided credentials are invalid."
            raise InfisicalCredentialsError(msg) from exc


class BaseInfisicalProvider(ABC):
    """Base class for Infisical credential providers.

    The base provider defines the interface for loading credentials and checking their validity.
    Its attributes are initialized to empty strings, and subclasses must implement the `_load` method
    to load credentials from their respective sources and overwrite the attributes accordingly.

    Attributes:
        url (str): The base URL for the Infisical API. Pulls from `INFISICAL_URL` or default.
        token (str): The JWT token for authentication.
        client_id (str): The client ID for refreshing the token.
        client_secret (str): The client secret for refreshing the token.
    """

    url: str = ""
    token: str = ""
    client_id: str = ""
    client_secret: str = ""

    @abstractmethod
    def _load(self) -> None:
        """Implement the provider-specific credentials loading method."""
        raise NotImplementedError

    def load(self, url: str = "") -> InfisicalCredentials | None:
        """Load the provided credentials.

        This method will call the `_load` method of the provider and return the credential object if valid.
        If the credentials are not valid, it will return None.
        If a `url` is provided, it will override the default URL for the provider.

        Args:
            url (str, optional): The base URL for the Infisical API. Defaults to "".
        """
        self.url = url.rstrip("/") if url else os.environ.get("INFISICAL_URL", "https://us.infisical.com").rstrip("/")
        self._load()
        credentials = InfisicalCredentials(
            url=self.url,
            token=self.token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        credentials.refresh()  # If the credentials are client id and secret, we need to refresh to get a token.
        if credentials.is_valid() and bool(credentials.get_token()):
            return credentials
        return None


class InfisicalConfigFileProvider(BaseInfisicalProvider):
    """Provides credentials from the Infisical configuration file.

    This provider uses the `FileKeyringBackend` to load the credentials from the keyring specified in the
    current user's config. This is typically `~/.infisical/infisical-config.json`. Currently, it will only
    load a `file` keyring vault backend.

    NOTE: Any explicitly or implicitly provided URL will be overwritten by the one in the config file.
    """

    def _load(self) -> None:
        """Load credentials from the Infisical configuration file."""
        config_file = FileKeyringBackend()
        jwt = config_file.get_password()
        if not jwt:
            return

        # The token is the JWE token stored in the keyring.
        self.token = jwt
        self.url = config_file.get_url()


class InfisicalEnvironmentProvider(BaseInfisicalProvider):
    """Provides credentials from environment variables.

    It will initially check for the `INFISICAL_TOKEN` environment variable. If it is not set, it will check for
    `INFISICAL_CLIENT_ID` and `INFISICAL_CLIENT_SECRET`. If both are set, it will use them to authenticate
    with the Infisical API and retrieve a token. If neither is set, it will return None.
    """

    def _load(self) -> None:
        if "INFISICAL_CLIENT_ID" in os.environ and "INFISICAL_CLIENT_SECRET" in os.environ:
            self.client_id = os.environ["INFISICAL_CLIENT_ID"]
            self.client_secret = os.environ["INFISICAL_CLIENT_SECRET"]
        elif "INFISICAL_TOKEN" in os.environ:
            self.token = os.environ["INFISICAL_TOKEN"]


class InfisicalExplicitProvider(BaseInfisicalProvider):
    """Provides explicitly passed credentials."""

    def __init__(self, token: str = "", client_id: str = "", client_secret: str = "") -> None:
        """Initialize the provider with explicit credentials."""
        self.token = token
        self.client_id = client_id
        self.client_secret = client_secret

    def _load(self) -> None:
        """Load credentials from explicitly provided values."""
        if not any([self.token, self.client_id, self.client_secret]):
            return

        if self.token and (self.client_id or self.client_secret):
            msg = "You may specify either a token or a Client ID and Secret, not both."
            raise InfisicalCredentialsError(msg)

        if not self.token and not all([self.client_id, self.client_secret]):
            msg = "Both Client ID and Secret must be provided."
            raise InfisicalCredentialsError(msg)


class InfisicalCredentialProviderChain:
    """Credential provider chain for Infisical.

    Tries to load credentials in the following order:
    1. Explicitly provided credentials
    2. Environment variables
    3. Configuration file.
    """

    providers: list[BaseInfisicalProvider]

    def __init__(
        self,
        url: str = "",
        token: str = "",
        client_id: str = "",
        client_secret: str = "",
    ) -> None:
        """Initialize the credential provider chain."""
        self.url = url
        self.providers = [
            InfisicalExplicitProvider(token=token, client_id=client_id, client_secret=client_secret),
            InfisicalEnvironmentProvider(),
            InfisicalConfigFileProvider(),
        ]

    def add_provider(self, provider: BaseInfisicalProvider, index: int = 0) -> None:
        """Add a provider to the chain.

        Args:
            provider (BaseInfisicalProvider): The provider to add.
            index (int, optional): The index at which to insert the provider in the chain. Defaults to 0.
        """
        self.providers.insert(index, provider)

    def resolve(self) -> InfisicalCredentials:
        """Resolve credentials using the provider chain."""
        for provider in self.providers:
            credentials = provider.load(url=self.url)
            if credentials:
                return credentials
        msg = "No valid Infisical credentials found in the provider chain."
        raise InfisicalCredentialsError(msg)
