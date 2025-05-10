"""Infisical Secrets Resource Models."""

import datetime
from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, Field

from infisical.resources.base import InfisicalResourceRequest

SecretType = Literal["shared", "personal"]


class ListSecretsQueryParams(TypedDict, total=False):
    """Query parameters for listing secrets."""

    environment: str
    expandSecretReferences: Literal["true", "false"]
    offset: int
    recursive: Literal["true", "false"]
    secretPath: str
    viewSecretValue: Literal["true", "false"]
    workspaceId: str
    workspaceSlug: str


class RetrieveSecretQueryParams(TypedDict, total=False):
    """Query parameters for retrieving a secret."""

    environment: str
    expandSecretReferences: Literal["true", "false"]
    include_imports: Literal["true", "false"]
    secretPath: str
    type: SecretType
    version: int
    viewSecretValue: Literal["true", "false"]
    workspaceId: str
    workspaceSlug: str


class Metadata(BaseModel):
    """Metadata model."""

    key: str
    value: str


class Tags(BaseModel):
    """Tags model."""

    id: str
    slug: str
    color: str
    name: str


class Secret(BaseModel):
    """Secret model."""

    _secret_id: Annotated[str, Field(alias="_id")]
    created_at: Annotated[datetime.datetime, Field(alias="createdAt")]
    environment: Annotated[str, Field()]
    folder_id: Annotated[str, Field(alias="folderId", default="")]
    is_rotated_secret: Annotated[bool | None, Field(alias="isRotatedSecret", default=None)]
    rotation_id: Annotated[str | None, Field(alias="rotationId", default=None)]
    secret_comment: Annotated[str, Field(alias="secretComment")]
    secret_id: Annotated[str, Field(alias="id")]
    secret_key: Annotated[str, Field(alias="secretKey")]
    secret_metadata: Annotated[list[Metadata] | None, Field(alias="secretMetadata", default=None)]
    secret_path: Annotated[str, Field(alias="secretPath", default="")]
    secret_reminder_note: Annotated[str | None, Field(alias="secretReminderNote", default=None)]
    secret_reminder_repeat_days: Annotated[int | None, Field(alias="secretReminderRepeatDays", default=None)]
    secret_type: Annotated[SecretType, Field(alias="type")]
    secret_value_hidden: Annotated[bool | None, Field(alias="secretValueHidden", default=None)]
    secret_value: Annotated[str, Field(alias="secretValue")]
    skip_multiline_encoding: Annotated[bool | None, Field(alias="skipMultilineEncoding", default=None)]
    tags: Annotated[list[Tags], Field(alias="tags", default_factory=list)]
    updated_at: Annotated[datetime.datetime, Field(alias="updatedAt")]
    user_id: Annotated[str | None, Field(alias="userId", default=None)]
    version: Annotated[int, Field()]
    workspace: Annotated[str, Field()]


class SecretsList(BaseModel):
    """List of secrets model."""

    imports: Annotated[list[dict], Field(default_factory=list)]
    secrets: Annotated[list[Secret], Field()]


class CreateSecretRequest(InfisicalResourceRequest):
    """Create secret request model."""

    name: Annotated[str, Field(exclude=True)]
    secret_comment: Annotated[str, Field(alias="secretComment", default="")]
    secret_metadata: Annotated[list[Metadata] | None, Field(alias="secretMetadata", default=None)]
    secret_path: Annotated[str, Field(alias="secretPath", default="/")]
    secret_reminder_note: Annotated[str | None, Field(alias="secretReminderNote", default=None, max_length=1024)]
    secret_reminder_repeat_days: Annotated[int | None, Field(alias="secretReminderRepeatDays", default=None)]
    secret_type: Annotated[SecretType, Field(alias="type", default="shared")]
    secret_value: Annotated[str, Field(alias="secretValue")]
    skip_multiline_encoding: Annotated[bool | None, Field(alias="skipMultilineEncoding", default=None)]
    tag_ids: Annotated[list[str] | None, Field(alias="tagIds", default=None)]


class UpdateSecretRequest(InfisicalResourceRequest):
    """Update secret request model."""

    metadata: Annotated[dict[str, str] | None, Field(alias="metadata", default=None)]
    name: Annotated[str, Field(exclude=True)]
    new_secret_name: Annotated[str | None, Field(alias="newSecretName", default=None, min_length=1)]
    secret_comment: Annotated[str | None, Field(alias="secretComment", default=None)]
    secret_metadata: Annotated[list[Metadata] | None, Field(alias="secretMetadata", default=None)]
    secret_path: Annotated[str, Field(alias="secretPath", default="/")]
    secret_reminder_note: Annotated[str | None, Field(alias="secretReminderNote", default=None, max_length=1024)]
    secret_reminder_recipients: Annotated[list[str] | None, Field(alias="secretReminderRecipients", default=None)]
    secret_reminder_repeat_days: Annotated[int | None, Field(alias="secretReminderRepeatDays", default=None)]
    secret_type: Annotated[SecretType, Field(alias="type", default="shared")]
    secret_value: Annotated[str | None, Field(alias="secretValue", default=None)]
    skip_multiline_encoding: Annotated[bool | None, Field(alias="skipMultilineEncoding", default=None)]
    tag_ids: Annotated[list[str] | None, Field(alias="tagIds", default=None)]


class DeleteSecretRequest(InfisicalResourceRequest):
    """Create secret request model."""

    name: Annotated[str, Field(exclude=True)]
    secret_path: Annotated[str, Field(alias="secretPath", default="/")]
    secret_type: Annotated[SecretType, Field(alias="type", default="shared")]


class SecretApprovalResponse(BaseModel):
    """Secret approval response model."""

    approval_id: Annotated[str, Field(alias="id")]
    bypass_reason: Annotated[str | None, Field(alias="bypassReason", default=None)]
    committer_user_id: Annotated[str, Field(alias="committerUserId")]
    conflicts: Annotated[Any, Field(alias="type", default=None)]
    created_at: Annotated[datetime.datetime, Field(alias="createdAt")]
    folder_id: Annotated[str, Field(alias="folderId")]
    has_merged: Annotated[bool, Field(alias="hasMerged", default=False)]
    is_replicated: Annotated[bool | None, Field(alias="isReplicated", default=None)]
    policy_id: Annotated[str, Field(alias="policyId")]
    slug: Annotated[str, Field(alias="slug")]
    status_changed_by_user_id: Annotated[str | None, Field(alias="statusChangedByUserId", default=None)]
    status: Annotated[str, Field()]
    updated_at: Annotated[datetime.datetime, Field(alias="updatedAt")]
