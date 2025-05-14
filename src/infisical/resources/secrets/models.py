"""Infisical Secrets Resource Models."""

import datetime
from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, Field

from infisical.resources.base import InfisicalResourceRequest

SecretType = Literal["shared", "personal"]


class ListSecretsQueryParams(TypedDict, total=False):
    """Query parameters for listing secrets.

    Other parameters:
        environment (str): The environment name. ***REQUIRED***
        expandSecretReferences (str): Whether to expand secret references.
        offset (int): The offset for pagination.
        recursive (str): Whether to list secrets recursively.
        secretPath (str): The path to the secret.
        viewSecretValue (str): Whether to view the secret value.
        workspaceId (str): The ID of the workspace. ***REQUIRED***
        workspaceSlug (str): The slug of the workspace.
    """

    environment: str
    expandSecretReferences: Literal["true", "false"]
    offset: int
    recursive: Literal["true", "false"]
    secretPath: str
    viewSecretValue: Literal["true", "false"]
    workspaceId: str
    workspaceSlug: str


class RetrieveSecretQueryParams(TypedDict, total=False):
    """Query parameters for retrieving a secret.

    Other parameters:
        environment (str): The environment name. ***REQUIRED***
        expandSecretReferences (str): Whether to expand secret references.
        include_imports (str): Whether to include imports.
        secretPath (str): The path to the secret.
        type (SecretType): The type of the secret.
        version (int): The version of the secret.
        viewSecretValue (str): Whether to view the secret value.
        workspaceId (str): The ID of the workspace. ***REQUIRED***
        workspaceSlug (str): The slug of the workspace.
    """

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
    """Metadata model.

    Attributes:
        key (str): The key of the metadata.
        value (str): The value of the metadata.
    """

    key: str
    value: str


class Tags(BaseModel):
    """Tags model.

    Attributes:
        id (str): The ID of the tag.
        slug (str): The slug of the tag.
        color (str): The color of the tag.
        name (str): The name of the tag.
    """

    id: str
    slug: str
    color: str
    name: str


class Secret(BaseModel):
    """Secret model.

    Attributes:
        _secret_id (str): The ID of the secret.
        created_at (datetime.datetime): The creation date of the secret.
        environment (str): The environment name.
        folder_id (str): The ID of the folder.
        is_rotated_secret (bool | None): Whether the secret is rotated.
        rotation_id (str | None): The ID of the rotation.
        secret_comment (str): The comment for the secret.
        secret_id (str): The ID of the secret.
        secret_key (str): The key of the secret.
        secret_metadata (list[Metadata] | None): The metadata of the secret.
        secret_path (str): The path to the secret.
        secret_reminder_note (str | None): The reminder note for the secret.
        secret_reminder_repeat_days (int | None): The number of days to repeat the reminder.
        secret_type (SecretType): The type of the secret.
        secret_value_hidden (bool | None): Whether the secret value is hidden.
        secret_value (str): The value of the secret.
        skip_multiline_encoding (bool | None): Whether to skip multiline encoding.
        tags (list[Tags]): The tags associated with the secret.
        updated_at (datetime.datetime): The last updated date of the secret.
        user_id (str | None): The ID of the user who created or updated the secret.
        version (int): The version of the secret.
        workspace (str): The workspace name.
    """

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
    """List of secrets model.

    Attributes:
        secrets (list[Secret]): The list of secrets.
        imports (list[dict]): The list of imports.
    """

    imports: Annotated[list[dict], Field(default_factory=list)]
    secrets: Annotated[list[Secret], Field()]


class CreateSecretRequest(InfisicalResourceRequest):
    """Create secret request model.

    Attributes:
        metadata (dict[str, str] | None): The metadata of the secret.
        name (str): The name of the secret.
        secret_comment (str): The comment for the secret.
        secret_metadata (list[Metadata] | None): The metadata of the secret.
        secret_path (str): The path to the secret.
        secret_reminder_note (str | None): The reminder note for the secret.
        secret_reminder_repeat_days (int | None): The number of days to repeat the reminder.
        secret_type (SecretType): The type of the secret.
        secret_value (str): The value of the secret.
        skip_multiline_encoding (bool | None): Whether to skip multiline encoding.
        tag_ids (list[str] | None): The IDs of the tags associated with the secret.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment name.
    """

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
    """Update secret request model.

    Attributes:
        metadata (dict[str, str] | None): The metadata of the secret.
        name (str): The name of the secret.
        new_secret_name (str | None): The new name of the secret.
        secret_comment (str | None): The comment for the secret.
        secret_metadata (list[Metadata] | None): The metadata of the secret.
        secret_path (str): The path to the secret.
        secret_reminder_note (str | None): The reminder note for the secret.
        secret_reminder_recipients (list[str] | None): The recipients of the reminder.
        secret_reminder_repeat_days (int | None): The number of days to repeat the reminder.
        secret_type (SecretType): The type of the secret.
        secret_value (str | None): The value of the secret.
        skip_multiline_encoding (bool | None): Whether to skip multiline encoding.
        tag_ids (list[str] | None): The IDs of the tags associated with the secret.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment name.
    """

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
    """Create secret request model.

    Attributes:
        name (str): The name of the secret.
        secret_path (str): The path to the secret.
        secret_type (SecretType): The type of the secret.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment name.
    """

    name: Annotated[str, Field(exclude=True)]
    secret_path: Annotated[str, Field(alias="secretPath", default="/")]
    secret_type: Annotated[SecretType, Field(alias="type", default="shared")]


class SecretApprovalResponse(BaseModel):
    """Secret approval response model.

    Attributes:
        approval_id (str): The ID of the approval.
        bypass_reason (str | None): The reason for bypassing the approval.
        committer_user_id (str): The ID of the user who committed the change.
        conflicts (Any): The conflicts associated with the approval.
        created_at (datetime.datetime): The creation date of the approval.
        folder_id (str): The ID of the folder.
        has_merged (bool): Whether the approval has been merged.
        is_replicated (bool | None): Whether the approval is replicated.
        policy_id (str): The ID of the policy.
        slug (str): The slug of the approval.
        status_changed_by_user_id (str | None): The ID of the user who changed the status.
        status (str): The status of the approval.
        updated_at (datetime.datetime): The last updated date of the approval.
    """

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
