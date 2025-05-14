import json
from pathlib import Path
import pytest
from infisical.credentials.keyring_handler import FileKeyringBackend
import tempfile
import base64


class TestFileKeyringBackend:
    def test_priority(self):
        keyring_handler = FileKeyringBackend()
        assert keyring_handler.priority == 69

    def test_config(self):
        keyring_handler = FileKeyringBackend()
        keyring_handler.CONFIG_FILE = Path("non_existent_path")
        assert isinstance(keyring_handler.config, dict)
        assert not keyring_handler.config  # Ensure config is empty

        keyring_handler = FileKeyringBackend()
        with tempfile.NamedTemporaryFile(mode="+wt") as temp_file:
            temp_file.write(json.dumps({
                "logged_in_user": "test_user",
                "keyring_password": "test_password"
            }))
            temp_file.seek(0)
            keyring_handler.CONFIG_FILE = Path(temp_file.name)
            assert isinstance(keyring_handler.config, dict)
            assert keyring_handler.config
            assert "logged_in_user" in keyring_handler.config
            assert "keyring_password" in keyring_handler.config

    @pytest.mark.parametrize("passphrase,user,backend,exists,expected", [
        ("test_password", "test_user", "file", True, "test_token"),
        ("test_password", "test_user", "auto", True, ""),
        ("test_password", "", "file", True, ""),
        ("", "test_user", "file", True, ""),
        ("test_password", "test_user", "file", False, ""),
    ])
    def test_get_password(self, passphrase: str, user: str, backend: str, expected: str, exists: bool, generate_jwe):
        config = {"vaultBackendType": backend}
        if passphrase:
            config["vaultBackendPassphrase"] = base64.b64encode(passphrase.encode()).decode()
        if user:
            config["loggedInUserEmail"] = user

        keyring_handler = FileKeyringBackend()
        with tempfile.NamedTemporaryFile(mode="+wt") as temp_file, tempfile.TemporaryDirectory() as temp_dir:
            temp_file.write(json.dumps(config))
            temp_file.seek(0)

            if exists:
                # If the user doesn't exist, we'll use a fake one to test existing behavior
                with Path(f"{temp_dir}/{user or 'foo'}").open("+wt") as keyring_file:
                    keyring_file.write(generate_jwe(passphrase, {"JTWToken": "test_token"}))

            keyring_handler.CONFIG_FILE = Path(temp_file.name)
            keyring_handler.KEYRING_PATH = Path(temp_dir)

            if backend == "auto":
                with pytest.warns(UserWarning):
                    token = keyring_handler.get_password()
            else:
                token = keyring_handler.get_password()
        
            assert token == expected

    @pytest.mark.parametrize("url", ["https://test.domain.example", "https://test.domain.example/api"])
    def test_get_url(self, url):
        keyring_handler = FileKeyringBackend()
        with tempfile.NamedTemporaryFile(mode="+wt") as temp_file:
            temp_file.write(json.dumps({"LoggedInUserDomain": url}))
            temp_file.seek(0)
            keyring_handler.CONFIG_FILE = Path(temp_file.name)
            assert keyring_handler.get_url()
            assert not keyring_handler.get_url().endswith("/api")

    def test_set_password(self):
        with pytest.raises(NotImplementedError):
            FileKeyringBackend().set_password("foo", "bar", "baz")
