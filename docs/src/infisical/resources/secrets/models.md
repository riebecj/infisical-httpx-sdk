# Models

[Infisical HTTPX SDK Documentation](../../../../README.md#infisical-httpx-sdk-documentation) / `src` / [Infisical](../../index.md#infisical) / [Resources](../index.md#resources) / [Secrets](./index.md#secrets) / Models

> Auto-generated documentation for [src.infisical.resources.secrets.models](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py) module.

- [Models](#models)
  - [CreateSecretRequest](#createsecretrequest)
  - [DeleteSecretRequest](#deletesecretrequest)
  - [ListSecretsQueryParams](#listsecretsqueryparams)
  - [Metadata](#metadata)
  - [RetrieveSecretQueryParams](#retrievesecretqueryparams)
  - [Secret](#secret)
  - [SecretApprovalResponse](#secretapprovalresponse)
  - [SecretsList](#secretslist)
  - [Tags](#tags)
  - [UpdateSecretRequest](#updatesecretrequest)

## CreateSecretRequest

[Show source in models.py:90](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L90)

Create secret request model.

#### Signature

```python
class CreateSecretRequest(InfisicalResourceRequest): ...
```



## DeleteSecretRequest

[Show source in models.py:123](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L123)

Create secret request model.

#### Signature

```python
class DeleteSecretRequest(InfisicalResourceRequest): ...
```



## ListSecretsQueryParams

[Show source in models.py:13](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L13)

Query parameters for listing secrets.

#### Signature

```python
class ListSecretsQueryParams(TypedDict): ...
```



## Metadata

[Show source in models.py:40](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L40)

Metadata model.

#### Signature

```python
class Metadata(BaseModel): ...
```



## RetrieveSecretQueryParams

[Show source in models.py:26](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L26)

Query parameters for retrieving a secret.

#### Signature

```python
class RetrieveSecretQueryParams(TypedDict): ...
```



## Secret

[Show source in models.py:56](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L56)

Secret model.

#### Signature

```python
class Secret(BaseModel): ...
```



## SecretApprovalResponse

[Show source in models.py:131](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L131)

Secret approval response model.

#### Signature

```python
class SecretApprovalResponse(BaseModel): ...
```



## SecretsList

[Show source in models.py:83](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L83)

List of secrets model.

#### Signature

```python
class SecretsList(BaseModel): ...
```



## Tags

[Show source in models.py:47](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L47)

Tags model.

#### Signature

```python
class Tags(BaseModel): ...
```



## UpdateSecretRequest

[Show source in models.py:105](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/secrets/models.py#L105)

Update secret request model.

#### Signature

```python
class UpdateSecretRequest(InfisicalResourceRequest): ...
```