# Providers

[Infisical HTTPX SDK Documentation](../../../README.md#infisical-httpx-sdk-documentation) / `src` / [Infisical](../index.md#infisical) / [Credentials](./index.md#credentials) / Providers

> Auto-generated documentation for [src.infisical.credentials.providers](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py) module.

- [Providers](#providers)
  - [BaseInfisicalProvider](#baseinfisicalprovider)
  - [InfisicalConfigFileProvider](#infisicalconfigfileprovider)
  - [InfisicalCredentialProviderChain](#infisicalcredentialproviderchain)
  - [InfisicalCredentials](#infisicalcredentials)
  - [InfisicalCredentialsError](#infisicalcredentialserror)
  - [InfisicalEnvironmentProvider](#infisicalenvironmentprovider)
  - [InfisicalExplicitProvider](#infisicalexplicitprovider)

## BaseInfisicalProvider

[Show source in providers.py:112](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L112)

Base class for Infisical credential providers.

The base provider defines the interface for loading credentials and checking their validity.
Its attributes are initialized to empty strings, and subclasses must implement the `_load` method
to load credentials from their respective sources and overwrite the attributes accordingly.

#### Attributes

- `url` *str* - The base URL for the Infisical API. Pulls from `INFISICAL_URL` or default.
- `token` *str* - The JWT token for authentication.
- `client_id` *str* - The client ID for refreshing the token.
- `client_secret` *str* - The client secret for refreshing the token.

#### Signature

```python
class BaseInfisicalProvider(ABC): ...
```

### BaseInfisicalProvider()._load

[Show source in providers.py:131](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L131)

Implement the provider-specific credentials loading method.

#### Signature

```python
@abstractmethod
def _load(self) -> None: ...
```

### BaseInfisicalProvider().load

[Show source in providers.py:136](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L136)

Load the provided credentials.

This method will call the `_load` method of the provider and return the credential object if valid.
If the credentials are not valid, it will return None.
If a [url](#baseinfisicalprovider) is provided, it will override the default URL for the provider.

#### Arguments

- [url](#baseinfisicalprovider) *str, optional* - The base URL for the Infisical API. Defaults to "".

#### Signature

```python
def load(self, url: str = "") -> InfisicalCredentials | None: ...
```



## InfisicalConfigFileProvider

[Show source in providers.py:160](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L160)

Provides credentials from the Infisical configuration file.

This provider uses the `FileKeyringBackend` to load the credentials from the keyring specified in the
current user's config. This is typically `~/.infisical/infisical-config.json`. Currently, it will only
load a `file` keyring vault backend.

NOTE: Any explicitly or implicitly provided URL will be overwritten by the one in the config file.

#### Signature

```python
class InfisicalConfigFileProvider(BaseInfisicalProvider): ...
```

#### See also

- [BaseInfisicalProvider](#baseinfisicalprovider)

### InfisicalConfigFileProvider()._load

[Show source in providers.py:170](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L170)

Load credentials from the Infisical configuration file.

#### Signature

```python
def _load(self) -> None: ...
```



## InfisicalCredentialProviderChain

[Show source in providers.py:221](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L221)

Credential provider chain for Infisical.

Tries to load credentials in the following order:
1. Explicitly provided credentials
2. Environment variables
3. Configuration file.

#### Signature

```python
class InfisicalCredentialProviderChain:
    def __init__(
        self,
        url: str = "",
        token: str = "",
        client_id: str = "",
        client_secret: str = "",
    ) -> None: ...
```

### InfisicalCredentialProviderChain().add_provider

[Show source in providers.py:247](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L247)

Add a provider to the chain.

#### Arguments

- `provider` *BaseInfisicalProvider* - The provider to add.
- `index` *int, optional* - The index at which to insert the provider in the chain. Defaults to 0.

#### Signature

```python
def add_provider(self, provider: BaseInfisicalProvider, index: int = 0) -> None: ...
```

#### See also

- [BaseInfisicalProvider](#baseinfisicalprovider)

### InfisicalCredentialProviderChain().resolve

[Show source in providers.py:256](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L256)

Resolve credentials using the provider chain.

#### Signature

```python
def resolve(self) -> InfisicalCredentials: ...
```

#### See also

- [InfisicalCredentials](#infisicalcredentials)



## InfisicalCredentials

[Show source in providers.py:18](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L18)

Represents Infisical credentials.

This can be initialized with a token, in which case it is ineligible for refresh.
If `client_id` and `client_secret` are provided, it can be refreshed by calling the auth endpoint
again with the client ID and secret.

An explicit `url` or provider-based `url` will always be preferred. If none is provided, it will default to
checking the `INFISICAL_URL` environment variable, ultimately defaulting to "https://us.infisical.com" if not set.

#### Signature

```python
class InfisicalCredentials:
    def __init__(
        self, url: str, token: str, client_id: str, client_secret: str
    ) -> None: ...
```

### InfisicalCredentials()._check_refresh

[Show source in providers.py:85](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L85)

Check if the credentials are expired, and refreshes them if available.

The token is either explicitly set by the provider, or it is set by the `refresh()` method called by the
provider. If the token is expired and refreshable, it will be refreshed. If it is not refreshable, an error will
be raised.

#### Signature

```python
def _check_refresh(self) -> None: ...
```

### InfisicalCredentials().get_token

[Show source in providers.py:51](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L51)

Get the JWT token.

#### Signature

```python
def get_token(self) -> str: ...
```

### InfisicalCredentials().is_valid

[Show source in providers.py:47](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L47)

Check if the credentials are valid.

#### Signature

```python
def is_valid(self) -> bool: ...
```

### InfisicalCredentials().refresh

[Show source in providers.py:60](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L60)

Refresh the credentials by calling the Infisical auth endpoint.

This method will only work if the credentials are refreshable, i.e., if `client_id` and `client_secret` are
provided. If the credentials are not refreshable, this method will do nothing.

#### Signature

```python
def refresh(self) -> None: ...
```

### InfisicalCredentials().refreshable

[Show source in providers.py:56](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L56)

Check if the credentials are refreshable.

#### Signature

```python
def refreshable(self) -> bool: ...
```



## InfisicalCredentialsError

[Show source in providers.py:14](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L14)

Base class for Infisical credentials errors.

#### Signature

```python
class InfisicalCredentialsError(Exception): ...
```



## InfisicalEnvironmentProvider

[Show source in providers.py:182](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L182)

Provides credentials from environment variables.

It will initially check for the `INFISICAL_TOKEN` environment variable. If it is not set, it will check for
`INFISICAL_CLIENT_ID` and `INFISICAL_CLIENT_SECRET`. If both are set, it will use them to authenticate
with the Infisical API and retrieve a token. If neither is set, it will return None.

#### Signature

```python
class InfisicalEnvironmentProvider(BaseInfisicalProvider): ...
```

#### See also

- [BaseInfisicalProvider](#baseinfisicalprovider)



## InfisicalExplicitProvider

[Show source in providers.py:198](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L198)

Provides explicitly passed credentials.

#### Signature

```python
class InfisicalExplicitProvider(BaseInfisicalProvider):
    def __init__(
        self, token: str = "", client_id: str = "", client_secret: str = ""
    ) -> None: ...
```

#### See also

- [BaseInfisicalProvider](#baseinfisicalprovider)

### InfisicalExplicitProvider()._load

[Show source in providers.py:207](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/credentials/providers.py#L207)

Load credentials from explicitly provided values.

#### Signature

```python
def _load(self) -> None: ...
```