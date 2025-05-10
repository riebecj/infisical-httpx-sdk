# Exceptions

[Infisical HTTPX SDK Documentation](./README.md#infisical-httpx-sdk-documentation) / Exceptions

> Auto-generated documentation for [exceptions](../src/infisical/exceptions.py) module.

## InfisicalHTTPError

[Show source in exceptions.py:4](../src/infisical/exceptions.py#L4)

Infisical HTTP error.

#### Signature

```python
class InfisicalHTTPError(Exception):
    def __init__(self, err_json: dict) -> None: ...
```

### InfisicalHTTPError().__err_type__

[Show source in exceptions.py:21](../src/infisical/exceptions.py#L21)

Return the error type based on the status code.

#### Signature

```python
def __err_type__(self, status_code: int) -> str: ...
```



## InfisicalResourceError

[Show source in exceptions.py:28](../src/infisical/exceptions.py#L28)

Custom exception for Infisical resource errors.

#### Signature

```python
class InfisicalResourceError(Exception): ...
```
