"""Infisical Client Credentials and Providers."""

import json
import os
import time
from abc import ABC, abstractmethod

import httpx
from jwcrypto.jwt import JWT, JWTExpired, JWTNotYetValid

from infisical.credentials.keyring_handler import FileKeyringBackend
from infisical.exceptions import InfisicalCredentialsError


class InfisicalCredentials:
    """Contains Infisical Credentials and methods to manage them.

    Supported authentication methods:

    - Token Auth: An already generated JWT token (e.g. [FileKeyringBackend][(p).keyring_handler.]).
    - [Universal Auth](https://infisical.com/docs/api-reference/endpoints/universal-auth/login)

    ???+ tip "Token Auth"

        This method is not eligible for refresh as there is no endpoint or mechanism to refresh the token. If
        you need to have refreshable credentials, you should use the Universal Auth method.

    An explicit `url` or provider-based `url` will always be preferred. If none is provided, it will default to
    checking the `INFISICAL_URL` environment variable, ultimately defaulting to `https://us.infisical.com` if not set.
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
        """Checks if the `_token` attribute is valid."""
        return bool(self._token)

    def get_token(self) -> str:
        """Get the JWT token.

        Calls [`__check_refresh__`][(c).] first before returning the token.

        Returns:
            str: The JWT token.
        """
        self.__check_refresh__()
        return self._token

    def refreshable(self) -> bool:
        """Check if the credentials are refreshable."""
        return self._refreshable

    def refresh(self) -> None:
        """Refresh the credentials if refreshable.

        Calls the [Login](https://infisical.com/docs/api-reference/endpoints/universal-auth/login) endpoint to refresh
        the credentials.

        ???+ tip "SSL Verification"

            By default, SSL verification is enabled. If you need to disable it, set the `INFISICAL_VERIFY_SSL`
            environment variable to `false`, `0`, or `no`; or pass the `verify_ssl` keyword argument to the client
            `__init__` set to `False`. This is ***not recommended*** in production environments.
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

    def __check_refresh__(self) -> None:
        """Check if the credentials are expired, and refreshes them if available.

        The token is either explicitly set by the provider, or it is set by the [`refresh`][(c).] method called by the
        provider. If the token is expired and refreshable, it will be refreshed. If it is not refreshable, it will
        raise an [InfisicalCredentialsError][src.infisical.exceptions.].

        Raises:
            InfisicalCredentialsError: If the credentials are invalid or expired and not refreshable.
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
    """Abstract Class for Infisical Credential Providers.

    This defines the interface for loading credentials and checking their validity.
    Its attributes are initialized to empty strings, and subclasses must implement the [`__load__`][(c).] method
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
    def __load__(self) -> None:
        """Implement the provider-specific credentials loading method.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError

    def load(self, url: str = "") -> InfisicalCredentials | None:
        """Load the provided credentials.

        This method will call the [`__load__`][(c).] method of the provider and return the credential object if valid.
        If the credentials are not valid, it will return None. If a `url` is provided, it will override the default
        URL for the provider. Otherwise, it checks the `INFISICAL_URL` environment variable and uses it if set.
        If the environment variable is not set, it will default to `https://us.infisical.com`.

        Args:
            url (str): The base URL for the Infisical API. Defaults to "".

        Returns:
            (InfisicalCredentials): If the provider finds correctly configured credentials.
            (None): If there are no credentials found for the provider.
        """
        self.url = url.rstrip("/") if url else os.environ.get("INFISICAL_URL", "https://us.infisical.com").rstrip("/")
        self.__load__()
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

    This provider uses the [FileKeyringBackend][(p).keyring_handler.] to load the credentials from the keyring
    specified in the current user's config. The config is typically found in `~/.infisical/infisical-config.json`.
    Currently, it will only load a `file` keyring [vault](https://infisical.com/docs/cli/commands/vault) backend.

    ???+ tip

        While it's not possible to refresh these credentials automatically, you can call the
        [`infisical login`](https://infisical.com/docs/cli/commands/login) command to refresh the credentials
        manually. This will update your keyring with a new token.
    """

    def __load__(self) -> None:
        """Load credentials from the [FileKeyringBackend][(p).keyring_handler.].

        !!! warning

            It is not possible to override the URL for this provider. The URL is always set to the one in the
            configuration file, as that is the endpoint that authorized the token.
        """
        config_file = FileKeyringBackend()
        jwt = config_file.get_password()
        if not jwt:
            return

        # The token is the JWE token stored in the keyring.
        self.token = jwt
        self.url = config_file.get_url()


class InfisicalEnvironmentProvider(BaseInfisicalProvider):
    """Provides credentials from environment variables.

    To use this with token authentication, set the `INFISICAL_TOKEN` environment variable to the token.
    For Universal Auth, set the `INFISICAL_CLIENT_ID` and `INFISICAL_CLIENT_SECRET` environment variables.
    """

    def __load__(self) -> None:
        """Load credentials from environment variables."""
        if "INFISICAL_CLIENT_ID" in os.environ and "INFISICAL_CLIENT_SECRET" in os.environ:
            self.client_id = os.environ["INFISICAL_CLIENT_ID"]
            self.client_secret = os.environ["INFISICAL_CLIENT_SECRET"]
        elif "INFISICAL_TOKEN" in os.environ:
            self.token = os.environ["INFISICAL_TOKEN"]


class InfisicalExplicitProvider(BaseInfisicalProvider):
    """Provides explicitly passed credentials.

    These are configured by passsing the `token` keyword argument or both the `client_id` and `client_secret`
    keyword arguments to the constructor of either the [InfisicalClient][src.infisical.clients.clients.] or the
    [InfisicalAsyncClient][src.infisical.clients.clients.].
    """

    def __init__(self, token: str = "", client_id: str = "", client_secret: str = "") -> None:
        """Initialize the provider with explicit credentials.

        ???+ note

            The credential keyword arguments are not required, as there are other providers in the chain, and *falsy*
            values are ignored. If values are provided, they will be validated in the [`__load__`][(c).] method.
        """
        self.token = token
        self.client_id = client_id
        self.client_secret = client_secret

    def __load__(self) -> None:
        """Load credentials from explicitly provided values, if the values are *truthy*.

        This method just ensures the values are set correctly and raises an error if they are not. Properly
        configured credentials means that either a token is set or both the client ID and secret are set.

        Raises:
            InfisicalCredentialsError: If the credentials are not set correctly.
        """
        if not any([self.token, self.client_id, self.client_secret]):
            return

        if self.token and (self.client_id or self.client_secret):
            msg = "You may specify either a token or a Client ID and Secret, not both."
            raise InfisicalCredentialsError(msg)

        if not self.token and not all([self.client_id, self.client_secret]):
            msg = "Both Client ID and Secret must be provided."
            raise InfisicalCredentialsError(msg)


class InfisicalCredentialProviderChain:
    """Credential provider chain for Infisical HTTPX SDK Clients.

    Tries to load credentials in the following order:

    1. Explicitly provided credentials
    2. Environment variables
    3. Configuration file.

    If no credentials are found in the first provider, it will try the next one in the chain.
    If no credentials are found in any provider, it will raise an
    [InfisicalCredentialsError][src.infisical.exceptions.]. Depending on the provider, misconfigured
    credentials may also raise an error.

    ???+ note

        The order of the providers is important. The explicit provider should always be first, as it is the most
        obvious way to get credentials, and the user can implement numerous mechanisms to securely pass
        credentials. The environment provider should be second, as it is the most typical and fairly secure way to
        get credentials even in CI/CD environments. The config file provider should be last, as it is `$USER`-specific
        and not always available. Especially considering that we are unable to refresh the credentials from the config
        file provider.

    Attributes:
        providers (list[BaseInfisicalProvider]): The list of providers in the chain.
        url (str): The base URL for the Infisical API passed in via `__init__.
    """

    providers: list[BaseInfisicalProvider]

    def __init__(
        self,
        url: str = "",
        token: str = "",
        client_id: str = "",
        client_secret: str = "",
    ) -> None:
        """Initialize the credential provider chain.

        Args:
            url (str): The base URL for the Infisical API.
            token (str): The JWT token for authentication.
            client_id (str): The client ID for refreshing the token.
            client_secret (str): The client secret for refreshing the token.

        ???+ tip

            The `url` kwyword argument can be passed to the constructor of either the
            [InfisicalClient][src.infisical.clients.clients.] or the
            [InfisicalAsyncClient][src.infisical.clients.clients.] which is passed into this constructor. If a *truthy*
            value is passed, it will override the default URL for every provider in the chain, ***except*** the
            [InfisicalConfigFileProvider][src.infisical.credentials.providers.].
        """
        self.url = url
        self.providers = [
            InfisicalExplicitProvider(token=token, client_id=client_id, client_secret=client_secret),
            InfisicalEnvironmentProvider(),
            InfisicalConfigFileProvider(),
        ]

    def add_provider(self, provider: BaseInfisicalProvider, index: int = 0) -> None:
        """Add a provider to the chain.

        This method allows you to add custom provider to the chain at a specific index. The default index is `0`,
        which means the provider will be added to the beginning of the chain. This is also useful if you want to
        override the default order of the providers.

        Args:
            provider (BaseInfisicalProvider): The provider to add.
            index (int, optional): The index at which to insert the provider in the chain. Defaults to 0.

        Example: Custom Provider Example
            ```python
            from infisical.credentials.providers import (
                BaseInfisicalProvider,
                InfisicalCredentialProviderChain,
            )

            class CustomProvider(BaseInfisicalProvider):
                def __load__(self) -> None:
                    ...
                    # Custom logic to load a `token` or `client_id` and `client_secret`

            provider_chain = InfisicalCredentialProviderChain()
            provider_chain.add_provider(CustomProvider())  # add provider to the beginning of the chain
            with InfisicalClient(provider_chain=provider_chain) as client:
                ...
                # Use the client with the custom provider
            ```
        """
        self.providers.insert(index, provider)

    def resolve(self) -> InfisicalCredentials:
        """Resolve credentials using the provider chain.

        This method will iterate through the providers in the chain and call their [`load`][(m).BaseInfisicalProvider.]
        method. If a provider returns a [InfisicalCredentials][(m).], it will return it (which is then set in the
        client). If no provider returns a valid credential, it will raise an
        [InfisicalCredentialsError][src.infisical.exceptions.].

        Raises:
            InfisicalCredentialsError: If no valid credentials are found in the provider chain.
        """
        for provider in self.providers:
            credentials = provider.load(url=self.url)
            if credentials:
                return credentials
        msg = "No valid Infisical credentials found in the provider chain."
        raise InfisicalCredentialsError(msg)
