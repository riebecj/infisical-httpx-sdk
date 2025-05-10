# Keyring Handler

[Infisical HTTPX SDK Documentation](../../../README.md#infisical-httpx-sdk-documentation) / `src` / [Infisical](../index.md#infisical) / [Credentials](./index.md#credentials) / Keyring Handler

> Auto-generated documentation for [src.infisical.credentials.keyring_handler](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py) module.

- [Keyring Handler](#keyring-handler)
  - [FileKeyringBackend](#filekeyringbackend)

## FileKeyringBackend

[Show source in keyring_handler.py:13](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py#L13)

A keyring backend that uses a file to store credentials.

This backend is designed to work with the Infisical configuration file
located at `~/.infisical/infisical-config.json`. It retrieves logged-in user
and keyring password information from this file. It then uses the
`infisical-keyring` directory in the user's home directory to access the
JWE token for the logged-in user.

#### Attributes

- `CONFIG_PATH` *Path* - The path to the Infisical configuration file.
- `KEYRING_PATH` *Path* - The path to the keyring file for the logged-in user.

#### Signature

```python
class FileKeyringBackend(KeyringBackend): ...
```

### FileKeyringBackend().config

[Show source in keyring_handler.py:41](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py#L41)

Read and cache the Infisical configuration file.

#### Signature

```python
@cached_property
def config(self) -> dict: ...
```

### FileKeyringBackend().get_password

[Show source in keyring_handler.py:49](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py#L49)

Retrieve a password from the keyring.

The arguments are not used in this implementation, as the keyring
is designed to store a single JWE token for the logged-in user, but
they are required by the KeyringBackend interface.

This method reads the Infisical configuration file and retrieves the JWE token
stored in the keyring file for the logged-in user. If the configuration file does
not exist, is misconfigured, or the vault backend type is not 'file', it returns an
empty string.

#### Returns

- `str` - The JWT token from the decrypted JWE token if available, otherwise an empty string.

#### Signature

```python
def get_password(self, _: str = "", __: str = "") -> str: ...
```

### FileKeyringBackend().get_url

[Show source in keyring_handler.py:89](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py#L89)

Get the URL of the logged-in user.

#### Signature

```python
def get_url(self) -> str: ...
```

### FileKeyringBackend().priority

[Show source in keyring_handler.py:30](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py#L30)

Returns the priority of this keyring backend.

Not really used, but required by the KeyringBackend interface.

#### Returns

- `float` - The priority of this keyring backend, set to 69 for fun.

#### Signature

```python
@property
def priority(self) -> float: ...
```

### FileKeyringBackend().set_password

[Show source in keyring_handler.py:96](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/keyring_handler.py#L96)

NOT USED.

This method is not implemented as the keyring is designed to retrieve
a single JWE token for the logged-in user, and setting passwords is not
supported in this implementation.

#### Arguments

- `service` - Unused argument.
- `username` - Unused argument.
- `password` - Unused argument.

#### Signature

```python
def set_password(self, service: str, username: str, password: str) -> None: ...
```