"""Infisical Keyring Handler."""

import base64
import json
import warnings
from functools import cached_property
from pathlib import Path

from jwcrypto.jwe import JWE
from keyring.backend import KeyringBackend


class FileKeyringBackend(KeyringBackend):
    """A keyring backend that uses a file to store credentials.

    This backend is designed to work with the Infisical configuration file
    located at `~/.infisical/infisical-config.json`. It retrieves logged-in user
    and keyring password information from this file. It then uses the
    `infisical-keyring` directory in the user's home directory to access the
    JWE token for the logged-in user.

    Attributes:
        CONFIG_FILE (Path): The path to the Infisical configuration file: `~/.infisical/infisical-config.json`.
        KEYRING_PATH (Path): The path to the keyring directory: `~/infisical-keyring`.
    """

    CONFIG_FILE = Path.home() / ".infisical" / "infisical-config.json"
    KEYRING_PATH = Path.home() / "infisical-keyring"

    @property
    def priority(self) -> float:
        """Returns the priority of this keyring backend.

        Not really used, but required by the
        [KeyringBackend](https://github.com/jaraco/keyring/blob/main/keyring/backend.py#L65) interface.

        Returns:
            float: The priority of this keyring backend.
        """
        return 69

    @cached_property
    def config(self) -> dict:
        """Read, cache, and return the value of `CONFIG_FILE`."""
        if self.CONFIG_FILE.exists():
            with self.CONFIG_FILE.open("rt") as config_file:
                return json.load(config_file)
        return {}

    def get_password(self, _: str = "", __: str = "") -> str:
        """Retrieve a password from the keyring.

        The arguments are not used in this implementation, as the keyring is designed to store a single
        JWE token for the logged-in user, but they are required by the
        [KeyringBackend](https://github.com/jaraco/keyring/blob/main/keyring/backend.py#L65) interface.

        This method checks the [config][(c).], initially checking the `vaultBackendType` is set to `'file``. It then
        checks that the `vaultBackendPassphrase` and `loggedInUserEmail` fields are present. Then it verifies the
        `loggedInUserEmail`'s keyring file exists. If all these checks pass, it reads and decrypts the JWE token from
        the keyring file and returns the JWT token contained within it. If any of these checks fail, it returns an empty
        string.

        Warnings:
            UserWarning: If the vault backend type is not `'file'`.

        Returns:
            (str): The JWT token from the decrypted JWE token if available, otherwise an empty string.
        """
        if self.config.get("vaultBackendType") != "file":
            # Later versions might support other vault backends, but for now we only support 'file'.
            warnings.warn(
                message="Only the 'file' vault backend is supported.",
                category=UserWarning,
                stacklevel=1,
            )
            return ""

        if "vaultBackendPassphrase" not in self.config or "loggedInUserEmail" not in self.config:
            # If the config file does not contain the necessary fields, return an empty string.
            return ""

        user: str = self.config["loggedInUserEmail"]
        if not (self.KEYRING_PATH / user).exists():
            # If the keyring file for the logged-in user does not exist, return an empty string.
            return ""

        # Using `jwcrypto` because `python-jose` does not support the necessary JWE algorithms.
        jwe = JWE()
        jwe.deserialize((self.KEYRING_PATH / user).open("rt").read())
        jwe.decrypt(base64.b64decode(self.config["vaultBackendPassphrase"]))
        payload: bytes = jwe.payload
        return json.loads(json.loads(payload.decode()))["JTWToken"]  # Yes, it's mis-spelled in Infisical's JWE.

    def get_url(self) -> str:
        """Get the URL of the logged-in user.

        Returns:
            (str): The URL set in `LoggedInUserDomain` in the [config][(c).] file.
        """
        endpoint: str = self.config["LoggedInUserDomain"]
        if endpoint and endpoint.endswith("/api"):
            return endpoint[:-4]  # Remove the trailing '/api' if present.
        return endpoint

    def set_password(self, service: str, username: str, password: str) -> None:
        """NOT USED.

        !!! warning

            This method is not implemented as the keyring is designed to retrieve
            a single JWE token for the logged-in user, and setting passwords is not
            supported in this implementation.

        Args:
            service: Unused argument.
            username: Unused argument.
            password: Unused argument.

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError
