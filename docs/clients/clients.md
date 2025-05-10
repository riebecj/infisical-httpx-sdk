# Clients

[Infisical HTTPX SDK Documentation](../README.md#infisical-httpx-sdk-documentation) / [Clients](./index.md#clients) / Clients

> Auto-generated documentation for [clients.clients](../../src/infisical/clients/clients.py) module.

## InfisicalAsyncClient

[Show source in clients.py:102](../../src/infisical/clients/clients.py#L102)

Infisical async HTTPX client.

#### Signature

```python
class InfisicalAsyncClient(BaseClient):
    def __init__(self, **kwargs: Unpack[InfisicalClientParams]) -> None: ...
```

### InfisicalAsyncClient().__aenter__

[Show source in clients.py:110](../../src/infisical/clients/clients.py#L110)

Enter the context manager and return the HTTPX async client.

#### Signature

```python
async def __aenter__(self) -> Self: ...
```

### InfisicalAsyncClient().__aexit__

[Show source in clients.py:114](../../src/infisical/clients/clients.py#L114)

Exit the context manager and close the HTTPX async client.

#### Signature

```python
async def __aexit__(self, exc_type, exc_value, traceback) -> None: ...
```

### InfisicalAsyncClient().close

[Show source in clients.py:118](../../src/infisical/clients/clients.py#L118)

Close the HTTPX async client.

#### Signature

```python
async def close(self) -> None: ...
```

### InfisicalAsyncClient().create_request

[Show source in clients.py:122](../../src/infisical/clients/clients.py#L122)

Create a Coroutine request for the resource.

This method generates a request for the resource using the HTTPX async client. It is similar to the
`create_request` method in the [InfisicalClient](#infisicalclient) class, but it returns a coroutine that will be awaited by
the [InfisicalAsyncClient().handle_request](#infisicalasyncclienthandle_request) method.

#### Arguments

- `method` *HttpxMethod* - The HTTPX client method name as a string to use for the request.
- `url` *str* - The URL to send the request to.
params (dict | None, optional): The query parameters to include in the request. Defaults to None.
body (dict | None, optional): The body of the request. Defaults to None.

#### Signature

```python
def create_request(
    self,
    method: HttpxMethod,
    url: str,
    params: dict | None = None,
    body: dict | None = None,
) -> Coroutine: ...
```

### InfisicalAsyncClient().handle_request

[Show source in clients.py:163](../../src/infisical/clients/clients.py#L163)

Handle the asynchronous request.

This method is similar to the `handle_request` method in the [InfisicalClient](#infisicalclient) class, but it awaits the
coroutine returned by the [InfisicalAsyncClient().create_request](#infisicalasyncclientcreate_request) method.

The `expected_responses` parameter is typically a dictionary containing a mapping of possible keys within the
response JSON to look for and the corresponding model to validate against. If None, the entire response JSON
will be returned, which could be `Any` type. If the key is an empty string, it will validate the entire
response JSON against the model. If none of the keys are found in the response JSON, it will raise a
`ValueError`.

#### Arguments

- `request` *Coroutine* - The coroutine to await.
expected_responses (dict[str, BaseModel] | None): The expected responses for the request.

#### Signature

```python
async def handle_request(
    self, request: Coroutine, expected_responses: dict[str, BaseModel] | None = None
) -> BaseModel | Any: ...
```



## InfisicalClient

[Show source in clients.py:14](../../src/infisical/clients/clients.py#L14)

Infisical HTTPX client.

#### Signature

```python
class InfisicalClient(BaseClient):
    def __init__(self, **kwargs: Unpack[InfisicalClientParams]) -> None: ...
```

### InfisicalClient().__enter__

[Show source in clients.py:22](../../src/infisical/clients/clients.py#L22)

Enter the context manager and return the HTTPX client.

#### Signature

```python
def __enter__(self) -> Self: ...
```

### InfisicalClient().__exit__

[Show source in clients.py:26](../../src/infisical/clients/clients.py#L26)

Exit the context manager and close the HTTPX client.

#### Signature

```python
def __exit__(self, exc_type, exc_value, traceback) -> None: ...
```

### InfisicalClient().close

[Show source in clients.py:30](../../src/infisical/clients/clients.py#L30)

Close the HTTPX client.

#### Signature

```python
def close(self) -> None: ...
```

### InfisicalClient().create_request

[Show source in clients.py:34](../../src/infisical/clients/clients.py#L34)

Create an anonymous function request for the resource.

This method generates a request for the resource using the HTTPX client. It is similar to the
`create_request` method in the [InfisicalAsyncClient](#infisicalasyncclient) class, but it returns a callable that will be called
by the [InfisicalClient().handle_request](#infisicalclienthandle_request) method.

#### Arguments

- `method` *HttpxMethod* - The HTTPX client method name as a string to use for the request.
- `url` *str* - The URL to send the request to.
params (dict | None, optional): The query parameters to include in the request. Defaults to None.
body (dict | None, optional): The body of the request. Defaults to None.

#### Signature

```python
def create_request(
    self,
    method: HttpxMethod,
    url: str,
    params: dict | None = None,
    body: dict | None = None,
) -> Callable: ...
```

### InfisicalClient().handle_request

[Show source in clients.py:80](../../src/infisical/clients/clients.py#L80)

Handle the synchronous request.

This method is similar to the `handle_request` method in the `InfisicalAsyncClass` class, but it calls the
anonymous synchronous function created in the [InfisicalClient().create_request](#infisicalclientcreate_request) method.

The `expected_responses` parameter is typically a dictionary containing a mapping of possible keys within the
response JSON to look for and the corresponding model to validate against. If None, the entire response JSON
will be returned, which could be `Any` type. If the key is an empty string, it will validate the entire
response JSON against the model. If none of the keys are found in the response JSON, it will raise a
`ValueError`.

#### Arguments

- `request` *Callable* - The callable to call.
expected_responses (dict[str, BaseModel] | None): The expected responses for the request.

#### Signature

```python
def handle_request(
    self, request: Callable, expected_responses: dict[str, BaseModel] | None = None
) -> BaseModel | Any: ...
```
