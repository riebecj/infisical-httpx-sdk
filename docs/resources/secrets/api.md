# Api

[Infisical HTTPX SDK Documentation](../../README.md#infisical-httpx-sdk-documentation) / [Resources](../index.md#resources) / [Secrets](./index.md#secrets) / Api

> Auto-generated documentation for [resources.secrets.api](../../../src/infisical/resources/secrets/api.py) module.

## Secrets

[Show source in api.py:102](../../../src/infisical/resources/secrets/api.py#L102)

Infisical Secrets Resource.

#### Signature

```python
class Secrets:
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```



## SecretsV3

[Show source in api.py:20](../../../src/infisical/resources/secrets/api.py#L20)

Infisical Secrets v3 API.

#### Signature

```python
class SecretsV3(InfisicalAPI):
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```

### SecretsV3().create

[Show source in api.py:29](../../../src/infisical/resources/secrets/api.py#L29)

Create a new secret.

#### Signature

```python
def create(self, request: CreateSecretRequest) -> Secret: ...
```

### SecretsV3().delete

[Show source in api.py:40](../../../src/infisical/resources/secrets/api.py#L40)

Delete a secret.

#### Signature

```python
def delete(self, request: DeleteSecretRequest) -> Secret: ...
```

### SecretsV3().list

[Show source in api.py:54](../../../src/infisical/resources/secrets/api.py#L54)

List all secrets.

This method lists all secrets in the provided `workspaceId` and `environment`, which are required parameters.
The `secretPath` parameter is optional and can be used to filter the secrets by a specific path. If `recursive`
is not set to true, which the default is `false`, the list of secrets will be only those in the `secretPath`.

NOTE: The `viewSecretValue` param is permanently set to `false` to avoid exposing secret values when listing.
    This is by design and is not configurable. If you need to get a secret value, use the [SecretsV3().retrieve](#secretsv3retrieve) method.

#### Signature

```python
def list(self, **params: Unpack[ListSecretsQueryParams]) -> SecretsList: ...
```

### SecretsV3().retrieve

[Show source in api.py:74](../../../src/infisical/resources/secrets/api.py#L74)

Retrieve a secret by Name.

This method retrieves a secret from the `secretPath` by its `name` in the provided `workspaceId` and
`environment`, which are required parameters. If the secret is not found in the `secretPath`, it will return a
404 error.

#### Signature

```python
def retrieve(self, name: str, **params: Unpack[RetrieveSecretQueryParams]) -> Secret: ...
```

### SecretsV3().update

[Show source in api.py:87](../../../src/infisical/resources/secrets/api.py#L87)

Update a secret.

#### Signature

```python
def update(self, request: UpdateSecretRequest) -> Secret: ...
```
