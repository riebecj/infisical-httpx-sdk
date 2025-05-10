# Api

[Infisical HTTPX SDK Documentation](../../../../README.md#infisical-httpx-sdk-documentation) / `src` / [Infisical](../../index.md#infisical) / [Resources](../index.md#resources) / [Folders](./index.md#folders) / Api

> Auto-generated documentation for [src.infisical.resources.folders.api](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py) module.

- [Api](#api)
  - [Folders](#folders)
  - [FoldersV1](#foldersv1)

## Folders

[Show source in api.py:79](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L79)

Infisical Folders Resource.

#### Signature

```python
class Folders:
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```



## FoldersV1

[Show source in api.py:18](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L18)

Infisical Folders v1 API Resource.

#### Signature

```python
class FoldersV1(InfisicalAPI):
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```

### FoldersV1().create

[Show source in api.py:27](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L27)

Create a new folder.

#### Signature

```python
def create(self, request: CreateFolderRequest) -> Folder: ...
```

### FoldersV1().delete

[Show source in api.py:38](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L38)

Delete a folder.

#### Signature

```python
def delete(self, request: DeleteFolderRequest) -> Folder: ...
```

### FoldersV1().get_by_id

[Show source in api.py:49](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L49)

Get a folder by ID.

#### Signature

```python
def get_by_id(self, folder_id: str) -> Folder: ...
```

### FoldersV1().list

[Show source in api.py:56](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L56)

List all folders.

#### Signature

```python
def list(self, **params: Unpack[ListFoldersQueryParams]) -> FoldersList: ...
```

### FoldersV1().update

[Show source in api.py:67](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/folders/api.py#L67)

Update a folder.

#### Signature

```python
def update(self, request: UpdateFolderRequest) -> Folder: ...
```