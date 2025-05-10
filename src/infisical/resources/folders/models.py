"""Infisical Folders Resource Models."""

import datetime
from typing import Annotated, TypedDict

from pydantic import BaseModel, Field

from infisical.resources.base import InfisicalResourceRequest


class ListFoldersQueryParams(TypedDict, total=False):
    """Query parameters for listing secrets."""

    environment: str
    lastSecretModified: datetime.datetime
    path: str
    recursive: bool
    workspaceId: str


class Environment(BaseModel):
    """Environment model."""

    env_id: Annotated[str, Field(alias="envId")]
    env_name: Annotated[str, Field(alias="envName")]
    env_slug: Annotated[str, Field(alias="envSlug")]


class Folder(BaseModel):
    """Folder model."""

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
    """Folders list model."""

    folders: Annotated[list[Folder], Field()]


class CreateFolderRequest(InfisicalResourceRequest):
    """Create Folder Request Model."""

    description: Annotated[str | None, Field(default=None)]
    name: Annotated[str, Field()]
    path: Annotated[str, Field(default="/")]


class DeleteFolderRequest(InfisicalResourceRequest):
    """Delete Folder request model."""

    folder_id_or_name: Annotated[str, Field(exclude=True)]
    path: Annotated[str, Field(default="/")]


class UpdateFolderRequest(InfisicalResourceRequest):
    """Update Folder request model."""

    description: Annotated[str | None, Field(default=None)]
    folder_id: Annotated[str, Field(exclude=True)]
    name: Annotated[str, Field()]
    path: Annotated[str, Field(default="/")]
