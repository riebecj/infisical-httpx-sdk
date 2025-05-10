"""Infisical client types."""

from typing import TYPE_CHECKING, Literal, TypedDict, TypeVar, Union

if TYPE_CHECKING:
    from infisical.clients.clients import InfisicalAsyncClient, InfisicalClient
    from infisical.credentials.providers import InfisicalCredentialProviderChain


HttpxMethod = Literal["get", "post", "put", "delete", "patch"]
SyncOrAsyncClient = TypeVar(
    "SyncOrAsyncClient",
    bound=Union["InfisicalClient", "InfisicalAsyncClient"],
)


class InfisicalClientParams(TypedDict, total=False):
    """Infisical client parameters."""

    endpoint: str
    token: str
    client_id: str
    client_secret: str
    verify_ssl: bool
    follow_redirects: bool
    provider_chain: "InfisicalCredentialProviderChain"
