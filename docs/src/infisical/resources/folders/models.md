# Models

[Infisical HTTPX SDK Documentation](../../../../README.md#infisical-httpx-sdk-documentation) / `src` / [Infisical](../../index.md#infisical) / [Resources](../index.md#resources) / [Folders](./index.md#folders) / Models

> Auto-generated documentation for [src.infisical.resources.folders.models](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py) module.

- [Models](#models)
  - [CreateFolderRequest](#createfolderrequest)
  - [DeleteFolderRequest](#deletefolderrequest)
  - [Environment](#environment)
  - [Folder](#folder)
  - [FoldersList](#folderslist)
  - [ListFoldersQueryParams](#listfoldersqueryparams)
  - [UpdateFolderRequest](#updatefolderrequest)

## CreateFolderRequest

[Show source in models.py:53](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L53)

Create Folder Request Model.

#### Signature

```python
class CreateFolderRequest(InfisicalResourceRequest): ...
```



## DeleteFolderRequest

[Show source in models.py:61](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L61)

Delete Folder request model.

#### Signature

```python
class DeleteFolderRequest(InfisicalResourceRequest): ...
```



## Environment

[Show source in models.py:21](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L21)

Environment model.

#### Signature

```python
class Environment(BaseModel): ...
```



## Folder

[Show source in models.py:29](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L29)

Folder model.

#### Signature

```python
class Folder(BaseModel): ...
```



## FoldersList

[Show source in models.py:47](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L47)

Folders list model.

#### Signature

```python
class FoldersList(BaseModel): ...
```



## ListFoldersQueryParams

[Show source in models.py:11](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L11)

Query parameters for listing secrets.

#### Signature

```python
class ListFoldersQueryParams(TypedDict): ...
```



## UpdateFolderRequest

[Show source in models.py:68](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/models.py#L68)

Update Folder request model.

#### Signature

```python
class UpdateFolderRequest(InfisicalResourceRequest): ...
```