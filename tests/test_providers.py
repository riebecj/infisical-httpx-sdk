import os
import pytest
from unittest.mock import patch

from infisical.credentials.providers import (
    BaseInfisicalProvider,
    InfisicalCredentials,
    InfisicalEnvironmentProvider,
    InfisicalConfigFileProvider,
    InfisicalExplicitProvider,
    InfisicalCredentialProviderChain,
    InfisicalCredentialsError
)

class TestInfisicalCredentials:
    def test_credentials_refreshable(self, generate_jwt):
        credentials = InfisicalCredentials(
            url="https://test.example", client_id="", client_secret="", token=generate_jwt()
        )
        assert not credentials.refreshable()
        assert credentials.get_token()

        credentials = InfisicalCredentials(
            url="https://test.example", client_id="test_client_id", client_secret="test_client_secret", token=""
        )
        assert credentials.refreshable()

    @patch(f"{InfisicalEnvironmentProvider.__module__}.httpx")
    def test_refresh(self, mock_httpx, generate_jwt):
        expired_token = generate_jwt("expired")
        new_token = generate_jwt()
        credentials = InfisicalCredentials(
            url="https://test.example", client_id="test_client_id", client_secret="test_client_secret", token=expired_token
        )
        mock_client = mock_httpx.Client.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {"accessToken": new_token}

        assert credentials.get_token() == new_token


class TestInfisicalProviders:
    @pytest.mark.parametrize("jwt_status,exception", [
        ("", None),
        ("invalid", InfisicalCredentialsError),
        ("expired", InfisicalCredentialsError),
        ("valid", None),
    ])
    @patch(f"{InfisicalConfigFileProvider.__module__}.FileKeyringBackend")
    def test_config_file_provider(self, mock_keyring, jwt_status, exception, generate_jwt):
        mock_keyring.return_value.get_password.return_value = generate_jwt(jwt_status) if jwt_status else ""
        mock_keyring.return_value.get_url.return_value = "https://test.example"

        if exception:
            with pytest.raises(exception):
                InfisicalConfigFileProvider().load()
        elif jwt_status:
            assert InfisicalConfigFileProvider().load()
        else:
            assert not InfisicalConfigFileProvider().load()

    def test_environment_provider_token(self, generate_jwt):
        os.environ["INFISICAL_TOKEN"] = generate_jwt()
        assert InfisicalEnvironmentProvider().load()
        del os.environ["INFISICAL_TOKEN"]
        assert not InfisicalEnvironmentProvider().load()

    @patch(f"{InfisicalEnvironmentProvider.__module__}.httpx")
    def test_environment_provider_universal_auth(self, mock_httpx, generate_jwt):
        mock_client = mock_httpx.Client.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {"accessToken": generate_jwt()}
        raise_for_status = mock_client.post.return_value.raise_for_status

        os.environ["INFISICAL_CLIENT_ID"] = "test_client_id"
        os.environ["INFISICAL_CLIENT_SECRET"] = "test_client_secret"
        provider = InfisicalEnvironmentProvider()
        assert provider.load()

        mock_client.post.assert_called_once_with(
            f"{provider.url}/api/v1/auth/universal-auth/login",
            json={
                "clientId": "test_client_id",
                "clientSecret": "test_client_secret",
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        raise_for_status.assert_called_once()

        del os.environ["INFISICAL_CLIENT_ID"]
        del os.environ["INFISICAL_CLIENT_SECRET"]
        assert not InfisicalEnvironmentProvider().load()

    @pytest.mark.parametrize("user_token,client_id,client_secret,exception", [
        (True, "test_client_id", "test_client_secret", InfisicalCredentialsError),
        (True, "test_client_id", "", InfisicalCredentialsError),
        (True, "", "test_client_secret", InfisicalCredentialsError),
        (False, "", "test_client_secret", InfisicalCredentialsError),
        (False, "test_client_id", "", InfisicalCredentialsError),
        (False, "test_client_id", "test_client_secret", None),
        (False, "", "", None),
    ])
    @patch(f"{InfisicalEnvironmentProvider.__module__}.httpx")
    def test_explicit_provider_token(self, mock_httpx, user_token, client_id, client_secret, exception, generate_jwt):
        token = generate_jwt() if user_token else ""
        
        mock_client = mock_httpx.Client.return_value.__enter__.return_value
        mock_client.post.return_value.json.return_value = {"accessToken": generate_jwt()}

        provider = InfisicalExplicitProvider(token=token, client_id=client_id, client_secret=client_secret)

        if exception:
            with pytest.raises(exception):
                provider.load()
        elif all([not user_token, not client_id, not client_secret]):
            assert not provider.load()
        else:
            assert provider.load()


class TestInfisicalCredentialProviderChain:
    class MockProvider(BaseInfisicalProvider):
        def _load(self):
            pass
        
    def test_add_provider(self):
        chain = InfisicalCredentialProviderChain()
        provider = self.MockProvider()
        chain.add_provider(provider, 1)
        assert chain.providers[1] == provider

    def test_resolve(self, generate_jwt):
        credentials = InfisicalCredentialProviderChain(token=generate_jwt()).resolve()
        assert isinstance(credentials, InfisicalCredentials)
        assert credentials.get_token()

        with pytest.raises(InfisicalCredentialsError):
            chain = InfisicalCredentialProviderChain()
            chain.providers = [self.MockProvider()]
            chain.resolve()
