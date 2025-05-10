# Base

[Infisical HTTPX SDK Documentation](../README.md#infisical-httpx-sdk-documentation) / [Clients](./index.md#clients) / Base

> Auto-generated documentation for [clients.base](../../src/infisical/clients/base.py) module.

## BaseClient

[Show source in base.py:23](../../src/infisical/clients/base.py#L23)

#### Attributes

- `client`: `httpx.Client | httpx.AsyncClient` - These are not a true class properties, but rather a placeholders to satisfy the type checker and provide a
  consistent interface for the clients. The properties are set in the `__set_apis__` method.


Infisical SDK Base Client.

This is the base class for both the synchronous and asynchronous clients. It handles the common functionality
between the two clients, such as creating requests, handling responses, and managing the credentials.
It is not meant to be used directly, but rather as a base class for the `InfisicalClient` and `InfisicalAsyncClient`
classes.

#### Signature

```python
class BaseClient:
    def __init__(self, **kwargs: Unpack[InfisicalClientParams]) -> None: ...
```

### BaseClient().__set_apis__

[Show source in base.py:49](../../src/infisical/clients/base.py#L49)

Set the APIs in a separate dunder method to keep the constructor clean.

#### Signature

```python
def __set_apis__(self) -> None: ...
```

### BaseClient()._get_headers

[Show source in base.py:56](../../src/infisical/clients/base.py#L56)

Generate the headers for the request.

The headers will include the `Authorization` header with the bearer token and the `Content-Type` header if
the method is not a GET request. The `Authorization` header will be set to the token from the credentials
acquired from the `InfisicalCredentialProviderChain`. We call `get_token()` every time to ensure we get a
valid token, as there is refresh logic in the credential object to handle token expiration.

NOTE: Token refreshing only happens if the credentials acquired are Universal Auth credentials (Client ID and
Secret). If the credentials are not Universal Auth credentials, the token cannot be refreshed and expiration
will raise an exception.

#### Signature

```python
def _get_headers(self, method: HttpxMethod) -> dict: ...
```

#### See also

- [HttpxMethod](#httpxmethod)

### BaseClient()._handle_response

[Show source in base.py:85](../../src/infisical/clients/base.py#L85)

Handle the response from the request.

The response object will raise an exception if the status code is not 2xx. If the status code is 4xx or 5xx,
it will raise an `InfisicalHTTPError` stacked with the `httpx.HTTPStatusError`. We will parse error response
JSON to provide more context about the error.

If the status code is 2xx, it will validate the response JSON against the expected responses, which is a dict
of response JSON keys to their corresponding models. If the key is an empty string, it will validate the
entire response JSON against the model. If none of the keys are found in the response JSON, it will raise a
`ValueError`.

#### Arguments

- `response` *httpx.Response* - The response object from the request.
expected_responses (dict[str, BaseModel]): A dict of response JSON keys to their corresponding models.

#### Returns

- `BaseModel` - The validated response model.
- `Any` - The raw response JSON if no expected responses are provided.

#### Signature

```python
def _handle_response(
    self,
    response: httpx.Response,
    expected_responses: dict[str, BaseModel] | None = None,
) -> BaseModel | Any: ...
```

### BaseClient().create_request

[Show source in base.py:74](../../src/infisical/clients/base.py#L74)

Abstract method to create a request for the resource.

#### Signature

```python
@abstractmethod
def create_request(
    self,
    method: HttpxMethod,
    url: str,
    params: dict | None = None,
    body: dict | None = None,
) -> Callable | Coroutine: ...
```

#### See also

- [HttpxMethod](#httpxmethod)
