# infisical-httpx-sdk
The Un-Official [Infisical](https://infisical.com/docs/documentation/getting-started/introduction) Python SDK using [HTTPX](https://www.python-httpx.org/).

There are two main reasons I created this repo despite an existing [official SDK](https://github.com/Infisical/python-sdk-official):

1) I wanted to utilize HTTPX for both synchronous and asynchronous HTTP calls, as I have use cases for both.
2) The implementation of a `boto`-esque credential provider chain that supports both Token and Universal auth credentials via:
    - Explicitly provided credentials at client creation.
    - Environment Variable credentials.
    - The `~/.infisical/infisical-config.json` keyring created when using the [`infisical login`](https://infisical.com/docs/cli/commands/login) CLI command.

Implementing all this over the top of the `requests` library currently used by the official SDK while trying to support sync and async clients would have required a re-architecture what they've already written, and I didn't feel like trying to climb that mountain nor ask them to oversee the climb. They're a busy company and I'm one guy.

## Table of Contents

- [Installation](#installation)

# Installation

The SDK is available on PyPI:

```
pip3 install infisical-httpx-sdk
```
