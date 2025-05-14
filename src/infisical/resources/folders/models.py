"""Infisical Folders Resource Models."""

import datetime
from typing import Annotated, TypedDict

from pydantic import BaseModel, Field

from infisical.resources.base import InfisicalResourceRequest


class ListFoldersQueryParams(TypedDict, total=False):
    """Query parameters for listing secrets.

    Thesre are the optional query parameters for the list secrets API.

    Other parameters:
        path (str): The path to the folder.
        recursive (bool): Whether to list secrets recursively.
        workspaceId (str): The ID of the workspace.
        environment (str): The environment name.
        lastSecretModified (datetime.datetime): The last modified date of the secret.
    """

    environment: str
    lastSecretModified: datetime.datetime
    path: str
    recursive: bool
    workspaceId: str


class Environment(BaseModel):
    """Environment model.

    Attributes:
        env_id (str): The ID of the environment.
        env_name (str): The name of the environment.
        env_slug (str): The slug of the environment.
    """

    env_id: Annotated[str, Field(alias="envId")]
    env_name: Annotated[str, Field(alias="envName")]
    env_slug: Annotated[str, Field(alias="envSlug")]


class Folder(BaseModel):
    """Folder model.

    Attributes:
        created_at (datetime.datetime): The creation date of the folder.
        description (str | None): The description of the folder.
        env_id (str): The ID of the environment.
        environment (Environment | None): The environment of the folder.
        folder_id (str): The ID of the folder.
        is_reserved (bool | None): Whether the folder is reserved.
        last_secret_modified (datetime.datetime | None): The last modified date of the secret.
        name (str): The name of the folder.
        parent_id (str | None): The ID of the parent folder.
        path (str | None): The path to the folder.
        project_id (str | None): The ID of the project.
        updated_at (datetime.datetime): The last updated date of the folder.
        version (int | None): The version of the folder.
    """

    created_at: Annotated[datetime.datetime, Field(alias="createdAt")]
    description: Annotated[str | None, Field(default=None)]
    env_id: Annotated[str, Field(alias="envId")]
    environment: Annotated[Environment | None, Field(default=None)]
    folder_id: Annotated[str, Field(alias="id")]
    is_reserved: Annotated[bool | None, Field(alias="isReserved", default=None)]
    last_secret_modified: Annotated[datetime.datetime | None, Field(alias="lastSecretModified", default=None)]
    name: Annotated[str, Field()]
    parent_id: Annotated[str | None, Field(alias="parentId", default=None)]
    path: Annotated[str | None, Field(default=None)]
    project_id: Annotated[str | None, Field(alias="projectId", default=None)]
    updated_at: Annotated[datetime.datetime, Field(alias="updatedAt")]
    version: Annotated[int | None, Field(default=None)]


class FoldersList(BaseModel):
    """Folders list model.

    Attributes:
        folders (list[Folder]): The list of folders.
    """

    folders: Annotated[list[Folder], Field()]


class CreateFolderRequest(InfisicalResourceRequest):
    """Create Folder Request Model.

    Attributes:
        description (str | None): The description of the folder.
        name (str): The name of the folder.
        path (str): The path to the folder.
    """

    description: Annotated[str | None, Field(default=None)]
    name: Annotated[str, Field()]
    path: Annotated[str, Field(default="/")]


class DeleteFolderRequest(InfisicalResourceRequest):
    """Delete Folder request model.

    The following are required when creating a new request:

        - `folder_id_or_name`: The ID or name of the folder to delete.
        - `workspace_id`: The ID of the workspace.
        - `environment`: The environment name.

    Attributes:
        folder_id_or_name (str): The ID or name of the folder to delete.
        path (str): The path to the folder.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment name.
    """

    folder_id_or_name: Annotated[str, Field(exclude=True)]
    path: Annotated[str, Field(default="/")]


class UpdateFolderRequest(InfisicalResourceRequest):
    """Update Folder request model.

    The following are required when creating a new request:

        - `folder_id`: The ID or name of the folder to delete.
        - `workspace_id`: The ID of the workspace.
        - `environment`: The environment name.

    Attributes:
        description (str | None): The description of the folder.
        folder_id (str): The ID of the folder to update.
        name (str | None): The name of the folder.
        path (str): The path to the folder.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment name.
    """

    description: Annotated[str | None, Field(default=None)]
    folder_id: Annotated[str, Field(exclude=True)]
    name: Annotated[str | None, Field(default=None)]
    path: Annotated[str, Field(default="/")]
