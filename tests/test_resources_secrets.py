import datetime
import pytest
from infisical.exceptions import InfisicalResourceError
from infisical.resources.secrets.api import Secrets, SecretsV3
from infisical.resources.secrets.models import (
    CreateSecretRequest,
    DeleteSecretRequest,
    UpdateSecretRequest,
    Secret,
    SecretsList,
    SecretApprovalResponse
)


class TestSecretsV3:
    test_secret = Secret(
        id="test_id",
        _id="test_id",
        workspace="workspace",
        environment="env",
        version=1,
        type="shared",
        secretKey="key",
        secretValue="value",
        secretComment="",
        createdAt=datetime.datetime.now(),
        updatedAt=datetime.datetime.now(),
    )
    test_approval = SecretApprovalResponse(
        id="test_id",
        policyId="policy_id",
        slug="slug",
        folderId="folder_id",
        createdAt=datetime.datetime.now(),
        updatedAt=datetime.datetime.now(),
        committerUserId="committer_user_id",
        status="test_status",
    )

    def test_create(self, mock_client, format_url):
        mock_client.handle_request.return_value = self.test_secret

        test_request = CreateSecretRequest(
            name="test_secret", secret_value="test_value", workspace_id="test_workspace", environment="test_env"
        )
        assert isinstance(SecretsV3(client=mock_client).create(test_request), Secret)

        mock_client.create_request.assert_called_once_with(
            method="post",
            url=format_url(SecretsV3, f"raw/{test_request.name}"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"secret": Secret}
        )

    @pytest.mark.parametrize("response,expected", [(test_secret, Secret), (test_approval, SecretApprovalResponse)])
    def test_delete(self, response, expected, mock_client, format_url):
        mock_client.handle_request.return_value = response

        test_request = DeleteSecretRequest(name="test_secret", workspace_id="test_workspace", environment="test_env")
        assert isinstance(SecretsV3(client=mock_client).delete(test_request), expected)

        mock_client.create_request.assert_called_once_with(
            method="delete",
            url=format_url(SecretsV3, f"raw/{test_request.name}"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"secret": Secret, "approval": SecretApprovalResponse},
        )

    @pytest.mark.parametrize("params,exception", [
        ({"workspaceId": "test_workspace"}, InfisicalResourceError),
        ({"environment": "test_env"}, InfisicalResourceError),
        ({"workspaceId": "test_workspace", "environment": "test_env"}, None),
    ])
    def test_list(self, params, exception, mock_client, format_url):
        mock_client.handle_request.return_value = SecretsList(secrets=[self.test_secret])

        if exception:
            with pytest.raises(exception):
                SecretsV3(client=mock_client).list(**params)
            mock_client.create_request.assert_not_called()
            mock_client.handle_request.assert_not_called()
        else:
            assert isinstance(SecretsV3(client=mock_client).list(**params), SecretsList)
            params["viewSecretValue"] = "false"
            mock_client.create_request.assert_called_once_with(
                method="get",
                url=format_url(SecretsV3, "/raw"),
                params=params,
            )
            mock_client.handle_request.assert_called_once_with(
                request=mock_client.create_request.return_value,
                expected_responses={"": SecretsList}
            )

    @pytest.mark.parametrize("params,exception", [
        ({"workspaceId": "test_workspace"}, InfisicalResourceError),
        ({"environment": "test_env"}, InfisicalResourceError),
        ({"workspaceId": "test_workspace", "environment": "test_env"}, None),
    ])
    def test_retrieve(self, params, exception, mock_client, format_url):
        mock_client.handle_request.return_value = self.test_secret

        if exception:
            with pytest.raises(exception):
                SecretsV3(client=mock_client).retrieve(name="test_secret", **params)
            mock_client.create_request.assert_not_called()
            mock_client.handle_request.assert_not_called()
        else:
            assert isinstance(SecretsV3(client=mock_client).retrieve(name="test_secret", **params), Secret)
            mock_client.create_request.assert_called_once_with(
                method="get",
                url=format_url(SecretsV3, "/raw/test_secret"),
                params=params,
            )
            mock_client.handle_request.assert_called_once_with(
                request=mock_client.create_request.return_value,
                expected_responses={"secret": Secret}
            )

    @pytest.mark.parametrize("response,expected", [(test_secret, Secret), (test_approval, SecretApprovalResponse)])
    def test_update(self, response, expected, mock_client, format_url):
        mock_client.handle_request.return_value = response

        test_request = UpdateSecretRequest(name="test_secret", workspace_id="test_workspace", environment="test_env")
        assert isinstance(SecretsV3(client=mock_client).update(test_request), expected)

        mock_client.create_request.assert_called_once_with(
            method="patch",
            url=format_url(SecretsV3, f"raw/{test_request.name}"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"secret": Secret, "approval": SecretApprovalResponse},
        )


class TestSecrets:
    def test_init(self, mock_client):
        secrets = Secrets(client=mock_client)
        assert isinstance(secrets.v3, SecretsV3)
        assert secrets.v3.client == mock_client
