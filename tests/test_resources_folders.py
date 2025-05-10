import datetime
import pytest

from infisical.exceptions import InfisicalResourceError
from infisical.resources.folders.api import Folders, FoldersV1
from infisical.resources.folders.models import DeleteFolderRequest, Environment, Folder, CreateFolderRequest, FoldersList, UpdateFolderRequest


class TestFoldersV1:
    test_folder = Folder(
        createdAt=datetime.datetime.now(),
        environment=Environment(envId="env_id", envName="env_name", envSlug="env_slug"),
        envId="env_id",
        id="folder_id",
        last_secret_modified=datetime.datetime.now(),
        name="Test Folder",
        updatedAt=datetime.datetime.now(),
    )

    def test_create(self, mock_client, format_url):
        mock_client.handle_request.return_value = self.test_folder

        test_request = CreateFolderRequest(
            name="test_folder", workspace_id="test_workspace", environment="test_env"
        )
        assert isinstance(FoldersV1(client=mock_client).create(test_request), Folder)
        mock_client.create_request.assert_called_once_with(
            method="post",
            url=format_url(FoldersV1, ""),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"folder": Folder},
        )
    
    def test_delete(self, mock_client, format_url):
        mock_client.handle_request.return_value = self.test_folder

        test_request = DeleteFolderRequest(
            folder_id_or_name="test_folder", workspace_id="test_workspace", environment="test_env"
        )
        assert isinstance(FoldersV1(client=mock_client).delete(test_request), Folder)
        mock_client.create_request.assert_called_once_with(
            method="delete",
            url=format_url(FoldersV1, f"/{test_request.folder_id_or_name}"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"folder": Folder},
        )

    def test_get_by_id(self, mock_client, format_url):
        mock_client.handle_request.return_value = self.test_folder

        folder_id = "test_folder_id"
        assert isinstance(FoldersV1(client=mock_client).get_by_id(folder_id=folder_id), Folder)
        mock_client.create_request.assert_called_once_with(
            method="get",
            url=format_url(FoldersV1, f"/{folder_id}"),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"folder": Folder},
        )

    @pytest.mark.parametrize("params,exception,check_isoformat", [
        ({"workspaceId": "test_workspace"}, InfisicalResourceError, False),
        ({"environment": "test_env"}, InfisicalResourceError, False),
        ({"workspaceId": "test_workspace", "environment": "test_env"}, None, False),
        ({"workspaceId": "test_workspace", "environment": "test_env"}, None, True),
    ])
    def test_list(self, params, exception, check_isoformat, mock_client, format_url):
        mock_client.handle_request.return_value = FoldersList(folders=[self.test_folder])

        if exception:
            with pytest.raises(exception):
                FoldersV1(client=mock_client).list(**params)
            mock_client.create_request.assert_not_called()
            mock_client.handle_request.assert_not_called()
        else:
            if check_isoformat:
                current_datetime = datetime.datetime.now()
                params["lastSecretModified"] = current_datetime

            assert isinstance(FoldersV1(client=mock_client).list(**params), FoldersList)

            if check_isoformat:
                params["lastSecretModified"] = current_datetime.isoformat()
            
            mock_client.create_request.assert_called_once_with(
                method="get",
                url=format_url(FoldersV1, "/"),
                params=params,
            )
            mock_client.handle_request.assert_called_once_with(
                request=mock_client.create_request.return_value,
                expected_responses={"": FoldersList}
            )

    def test_update(self, mock_client, format_url):
        mock_client.handle_request.return_value = self.test_folder

        test_request = UpdateFolderRequest(
            name="test_folder", folder_id="test_id", workspace_id="test_workspace", environment="test_env"
        )
        assert isinstance(FoldersV1(client=mock_client).update(test_request), Folder)
        mock_client.create_request.assert_called_once_with(
            method="patch",
            url=format_url(FoldersV1, f"/{test_request.folder_id}"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"folder": Folder},
        )


class TestFolders:
    def test_init(self, mock_client):
        folders = Folders(client=mock_client)
        assert isinstance(folders.v1, FoldersV1)
        assert folders.v1.client == mock_client
