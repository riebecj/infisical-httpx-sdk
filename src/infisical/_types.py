"""Infisical HTTPX SDK Types."""

from typing import TYPE_CHECKING, TypedDict, TypeVar, Union

if TYPE_CHECKING:
    from infisical.clients.clients import InfisicalAsyncClient, InfisicalClient
    from infisical.credentials.providers import InfisicalCredentialProviderChain


SyncOrAsyncClient = TypeVar(
    "SyncOrAsyncClient",
    bound=Union["InfisicalClient", "InfisicalAsyncClient"],
)


class InfisicalClientParams(TypedDict, total=False):
    """Infisical Client Parameters.

    The table below represents the available parameters you can pass to the
    [InfisicalClient][src.infisical.clients.clients.] and [InfisicalAsyncClient][src.infisical.clients.clients.]
    classes.

    | keyword | type |
    | ------- | ---- |
    | `endpoint` | `str` |
    | `token` | `str` |
    | `client_id` | `str` |
    | `client_secret` | `str` |
    | `verify_ssl` | `bool` |
    | `follow_redirects` | `bool` |
    | `provider_chain` | [InfisicalCredentialProviderChain][src.infisical.credentials.providers.] |
    """

    endpoint: str
    token: str
    client_id: str
    client_secret: str
    verify_ssl: bool
    follow_redirects: bool
    provider_chain: "InfisicalCredentialProviderChain"
