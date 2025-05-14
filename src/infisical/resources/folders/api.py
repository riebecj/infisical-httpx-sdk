"""Infisical Folders Resource API."""

from typing import Final, Unpack

from infisical._types import SyncOrAsyncClient
from infisical.resources.base import InfisicalAPI

from .models import (
    CreateFolderRequest,
    DeleteFolderRequest,
    Folder,
    FoldersList,
    ListFoldersQueryParams,
    UpdateFolderRequest,
)


class FoldersV1(InfisicalAPI):
    """Infisical Folders v1 API Resource.

    Attributes:
        base_uri (str): `/v1/folders`
    """

    base_uri: Final = "/v1/folders"

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Folders Resource.

        Args:
            client (SyncOrAsyncClient): An initialized [InfisicalClient][src.infisical.clients.clients.] or
                [InfisicalAsyncClient][src.infisical.clients.clients.].
        """
        super().__init__(client=client)

    def create(self, request: CreateFolderRequest) -> Folder:
        """Create a new folder.

        Args:
            request (CreateFolderRequest): The request object containing folder details.
        """
        self.logger.info("Creating folder %s", request.name)
        url = self._format_url("")  # Create uses the base URI
        _request = self.client.create_request(
            method="post",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(request=_request, expected_responses={"folder": Folder})

    def delete(self, request: DeleteFolderRequest) -> Folder:
        """Delete a folder.

        Args:
            request (DeleteFolderRequest): The request object containing folder ID or name.
        """
        self.logger.info("Deleting folder %s", request.folder_id_or_name)
        url = self._format_url(f"/{request.folder_id_or_name}")
        _request = self.client.create_request(
            method="delete",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(request=_request, expected_responses={"folder": Folder})

    def get_by_id(self, *, folder_id: str) -> Folder:
        """Get a folder by ID.

        Args:
            folder_id (str): The ID of the folder to retrieve.
        """
        self.logger.info("Getting folder by ID %s", folder_id)
        url = self._format_url(f"/{folder_id}")
        request = self.client.create_request(method="get", url=url)
        return self.client.handle_request(request=request, expected_responses={"folder": Folder})

    def list(self, **params: Unpack[ListFoldersQueryParams]) -> FoldersList:
        """List all folders.

        Args:
            **params (ListFoldersQueryParams): Optional query parameters for filtering the folder list.
        """
        self.logger.info("Listing folders with params %s", params)
        self.verify_required_params(required_params=["workspaceId", "environment"], params=params)
        if "lastSecretModified" in params:
            # Convert datetime to ISO format if present
            params["lastSecretModified"] = params["lastSecretModified"].isoformat()
        url = self._format_url("")
        request = self.client.create_request(method="get", url=url, params=params)
        return self.client.handle_request(request=request, expected_responses={"": FoldersList})

    def update(self, request: UpdateFolderRequest) -> Folder:
        """Update a folder.

        Args:
            request (UpdateFolderRequest): The request object containing folder ID and update details.
        """
        self.logger.info("Updating folder %s", request.folder_id)
        url = self._format_url(f"/{request.folder_id}")
        _request = self.client.create_request(
            method="patch",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(request=_request, expected_responses={"folder": Folder})


class Folders:
    """Infisical Folders Resource.

    Attributes:
        v1 (FoldersV1): The v1 API resource for folders.
    """

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Folders Resource.

        Args:
            client (SyncOrAsyncClient): An initialized [InfisicalClient][src.infisical.clients.clients.] or
                [InfisicalAsyncClient][src.infisical.clients.clients.].
        """
        self.v1 = FoldersV1(client=client)
