"""Infisical Secrets Resource API."""

from typing import Final, Unpack

from infisical._types import SyncOrAsyncClient
from infisical.resources.base import InfisicalAPI

from .models import (
    CreateSecretRequest,
    DeleteSecretRequest,
    ListSecretsQueryParams,
    RetrieveSecretQueryParams,
    Secret,
    SecretApprovalResponse,
    SecretsList,
    UpdateSecretRequest,
)


class SecretsV3(InfisicalAPI):
    """Infisical Secrets v3 API.

    Attributes:
        base_uri (str): `/v3/secrets`
    """

    base_uri: Final = "/v3/secrets"

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Secrets Resource.

        Args:
            client (SyncOrAsyncClient): An initialized [InfisicalClient][src.infisical.clients.clients.] or
                [InfisicalAsyncClient][src.infisical.clients.clients.].
        """
        super().__init__(client=client)

    def create(self, request: CreateSecretRequest) -> Secret:
        """Create a new secret.

        Args:
            request (CreateSecretRequest): The request object containing secret details.
        """
        self.logger.info("Creating secret %s", request.name)
        url = self._format_url(f"/raw/{request.name}")
        _request = self.client.create_request(
            method="post",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(request=_request, expected_responses={"secret": Secret})

    def delete(self, request: DeleteSecretRequest) -> Secret:
        """Delete a secret.

        Args:
            request (DeleteSecretRequest): The request object containing secret ID or name.
        """
        self.logger.info("Deleting secret %s", request.name)
        url = self._format_url(f"/raw/{request.name}")
        _request = self.client.create_request(
            method="delete",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(
            request=_request,
            expected_responses={"secret": Secret, "approval": SecretApprovalResponse},
        )

    def list(self, **params: Unpack[ListSecretsQueryParams]) -> SecretsList:
        """List all secrets.

        This method lists all secrets in the provided `workspaceId` and `environment`, which are required parameters.
        The `secretPath` parameter is optional and can be used to filter the secrets by a specific path. If `recursive`
        is not set to true, which the default is `false`, the list of secrets will be only those in the `secretPath`.

        Args:
            **params: (ListSecretsQueryParams): The query parameters for the request.

        !!! note

            The `viewSecretValue` param is permanently set to `false` to avoid exposing secret values when listing.
            This is by design and is not configurable. If you need to get a secret value, use the `retrieve` method.
        """
        self.logger.info("Listing secrets with params %s", params)
        self.verify_required_params(required_params=["workspaceId", "environment"], params=params)
        # Infisical defaults "viewSecretValue" to true, but we want it to be false because getting a secret value
        # should be an explicit action for a single secret and not the default for listing numerous secrets.
        # Maybe we can change this in the future, but for now, we will set it to false.
        params["viewSecretValue"] = "false"
        url = self._format_url("/raw")
        request = self.client.create_request(method="get", url=url, params=params)
        return self.client.handle_request(request=request, expected_responses={"": SecretsList})

    def retrieve(self, *, name: str, **params: Unpack[RetrieveSecretQueryParams]) -> Secret:
        """Retrieve a secret by Name.

        This method retrieves a secret from the `secretPath` by its `name` in the provided `workspaceId` and
        `environment`, which are required parameters. If the secret is not found in the `secretPath`, it will return a
        404 error.
        """
        self.logger.info("Retrieving secret %s with params %s", name, params)
        self.verify_required_params(required_params=["workspaceId", "environment"], params=params)
        url = self._format_url(f"/raw/{name}")
        request = self.client.create_request(method="get", url=url, params=params)
        return self.client.handle_request(request=request, expected_responses={"secret": Secret})

    def update(self, request: UpdateSecretRequest) -> Secret:
        """Update a secret."""
        self.logger.info("Updating secret %s", request.name)
        url = self._format_url(f"/raw/{request.name}")
        request = self.client.create_request(
            method="patch",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(
            request=request,
            expected_responses={"secret": Secret, "approval": SecretApprovalResponse},
        )


class Secrets:
    """Infisical Secrets Resource.

    Attributes:
        v3 (SecretsV3): The Infisical Secrets v3 API.
    """

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Secrets Resource.

        Args:
            client (SyncOrAsyncClient): An initialized [InfisicalClient][src.infisical.clients.clients.] or
                [InfisicalAsyncClient][src.infisical.clients.clients.].
        """
        self.v3 = SecretsV3(client=client)
