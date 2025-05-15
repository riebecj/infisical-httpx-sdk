# Infisical HTTPX SDK Documentation

The Un-Official [Infisical](https://infisical.com/docs/documentation/getting-started/introduction) Python SDK using [HTTPX](https://www.python-httpx.org/). Check out the [docs](https://riebecj.github.io/infisical-httpx-sdk/) for more information.

There are two main reasons I created this repo despite an existing [official SDK](https://github.com/Infisical/python-sdk-official):

1. I wanted to utilize HTTPX for both synchronous and asynchronous HTTP calls, as I have use cases for both.

2. The implementation of a `boto`-esque credential provider chain that supports both Token and Universal auth credentials via:
    - Explicitly provided credentials at client creation.
    - Environment Variable credentials.
    - The `~/.infisical/infisical-config.json` keyring created when using the [`infisical login`](https://infisical.com/docs/cli/commands/login) CLI command.

Implementing all this over the top of the `requests` library currently used by the official SDK while trying to support sync and async clients would have required a re-architecture what they've already written, and I didn't feel like trying to climb that mountain nor ask them to oversee the climb. They're a busy company and I'm one guy.

---

## Installation

The SDK is available on [PyPI](https://pypi.org/project/infisical-httpx-sdk/).

```bash
pip3 install infisical-httpx-sdk
```

## Clients

Since this SDK uses HTTPX for HTTP transport, it support both synchronous and asynchronous clients. Continue reading to learn more about how to create and use the clients.

### Create A Client

Creating a client is as simple as importing your desired client `InfisicalClient` or `InfisicalAsyncClient`.

```python
from infisical import InfisicalClient

# Token Auth
client = InfisicalClient(token="token", ...)

# Universal Auth
client = InfisicalClient(client_id="client_id", client_secret="client_secret", ...)
```

Instantiating the client works the same whether it's synchronous or asynchronous.

The only exception is if you use the clients in `with ...` context:

```python
from infisical import InfisicalClient, InfisicalAsyncClient

with InfisicalClient(token="token", ...) as client:
    ... # Call API client methods here

async with InfisicalAsyncClient(token="token", ...) as client:
    ... # await client API methods here
```

The benefit being if you use it within a context manager, exiting the context manager will automatically close the client, otherwise you will need to call `client.close()` or `await client.close()` to ensure the HTTPX client closes properly.

### Authenticating a Client

For a full list of currently available credential providers, see [Credential Providers](#credential-providers). 

In this example, we'll be using Universal Auth credentials, which are Client ID and Secret pairs. This is typically what you'd use in SDK integrations, as it is tied to machine identities in Infisical. These are also preferred for long-running SDK uses -- like a daemon process or your own API integration as a secrets backend -- as `InfisicalCredentials` using Universal Auth can automatically refresh the acquired auth token when it expires. 

You can explicitly provide the credentials like this:

```python
from infisical import InfisicalClient

client = InfisicalClient(client_id="client_id", client_secret="client_secret")
```

> NOTE: Hardcoding credentials in ***NEVER*** recommended. While it can be used for development purposes, it is recommended -- even in development -- to either set Environment Variables (ephemeral) or utilize the CLI via `infisical login` and let the provider chain use your keyring (encrypted).

Other authentication methods may be added later, so please check back later, request one be added via GitHub Issue, or even submit a PR!

### Call an API Resource

While there are some API resources available, and many more yet to be added, calling them is fairly straight forward, as they follow the [API Reference](https://infisical.com/docs/api-reference/overview/introduction) in terms of naming conventions. 

For example, the [Secrets](https://infisical.com/docs/api-reference/endpoints/secrets/list) endpoint resource is used to interact with secrets inside your Infisical. So, you access the resource methods via the `client.secrets` property. Given the first method is `List`, which lists the available secrets, you call the endpoint with `client.secrets.list()`.

> Note: Before you start calling endpoints willy-nilly, bear in mind that there will be some required arguments or keyword arguments you must provide to the function call. In the `list()` example above, the documentation does not specify that a `workspaceId` or `environment` is required. However, not providing them always returns a `4XX`. So, I've implemented a basic validation check for required parameters before making the call which will raise a `InfisicalResourceError` if the required query parameters are not provided. This is an effort to reduce the number of calls to APIs that we know are invalid.

In keeping with the same `list()` example, here's how it would look in your code to print a list of secrets in the root `/` of the project with a given project (workspace) ID and environment:

```python
from infisical import InfisicalClient

with InfisicalClient(token="token") as client:
    # `uuid` should be a real UUID and `env` should be your environment slug
    secrets = client.secrets.list(workspaceId="uuid", environment="env")
    for secret in secrets.secrets:
        print(secret.secret_key)
```


## Credential Providers

Given the multitude of methods to provide credentials to a process, the SDK utilizes a credential provider chain that iterates through the various methods in this order:

1) **Explicitly Provided**: These are passed as a(n) keyword argument(s) to the client constructor.
2) **Environment Variables**: Set in your current shell/daemon environment based on your OS type.
3) **Infisical Config**: This is created when using the Infisical CLI `infisical login` command. 

The first two providers accept either a Universal Auth Client ID and Secret, or a Token. In the given chain, if neither set of credentials are found, it will move on to the next provider. Should no credentials be found in *any* provider, it will raise an `InfisicalCredentialsError` exception.

The Universal Auth credentials are preferred as it allows the SDK to refresh your credentials on token expiration. When the provider chain resolves the Universal Auth credentials it finds, it calls the [Universal Auth](https://infisical.com/docs/api-reference/endpoints/universal-auth/login) endpoint to acquire a JWT that it uses when making API calls via the `Authorization: Bearer ...` header. Each call validates the JWT and expiration will trigger a refresh before setting the token in the header.

Using Token Auth is allowed, but since there is no mechanism for refreshing a JWT, an expired token raises an `InfisicalCredentialsError` exception. 

>NOTE: There is a [JWT Auth Login](https://infisical.com/docs/api-reference/endpoints/jwt-auth/login) endpoint which might provide a mechanism for refreshing a token-based credential but I have not looked into it yet.

### Explicit Credentials

This method is ***NOT RECOMMENDED*** for use in production unless you're using some other secure place to acquire the credentials before passing them in via variables and not hardcoded strings (e.g. using an EC2 Instance Profile to get them from AWS Secrets Manager).

Here's an example that gets them from AWS Secrets Manager:

```python
# Let's be secure about how we explicitly pass credentials
import json
import boto3
from infisical import InfisicalClient

identity = json.loads(
    boto3.client("secretsmanager").get_secret_value(SecretId="MyInfisicalIdentity")["SecretString"]
)
client = InfisicalClient(client_id=identity["client_id"], client_secret=identity["client_secret"])
```

If you're worried about you or someone you work with accidentally committing hardcoded secrets, check out Infisical's [Secret Scanning](https://infisical.com/docs/documentation/platform/secret-scanning) that integrates with your GitHub or the [CLI Secret Scanner](https://infisical.com/docs/cli/scanning-overview#automatically-scan-changes-before-you-commit) to scan your project before committing!

### Environment Variables

Self explanatory, this looks for the `INFISICAL_CLIENT_ID` and `INFISICAL_CLIENT_SECRET` in the OS environment, or `INFISICAL_TOKEN`. It is possible to set all three in your environment before initializing a client but it is **recommended** to only set one or the other. Universal Auth credentials are the preferred credentials, and will always be used if they are found. If they are not found, it will look for a token.


### Infisical Config

This provider looks for a `~/.infisical/infisical-config.json` file, which is created when using the [`infisical login`](https://infisical.com/docs/cli/commands/login) CLI command and the [vault](https://infisical.com/docs/cli/commands/vault) is set to `file`. This is similar to the [AWS CLI config file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) in that this SDK can utilize the settings stored within it and the JWE stored in the keyring file to access the correct auth token.

>CAUTION: This method is meant for use by the user logged in to the local machine and performs all API calls as that specified user. An expired token in the JWE will raise an exception, and the user must perform `infisical login` again to refresh it manually. Which is why it is recommended to use Universal Auth credentials for production.


>NOTE: The current SDK does not currently support the `auto` vault, which is based on the available kernel keyring.

### Custom Provider

Should you wish to create your own credential provider and add it to the chain, you can do so by inheriting from `BaseInfisicalProvider` and setting the `_load()` abstract method in your provider. 

```python
from infisical.credentials.providers import BaseInfisicalProvider

class MyProvider(BaseInfisicalProvider):
    def _load(self) -> None:
        # Load Universal Auth credentials here
        self.client_id = ...
        self.client_secret = ...

        # Or an already generated token
        self.token = ...
        
        # You can also include a mechanism for setting the Infisical base URL.
        # Default for all providers is the `INFISICAL_URL` environment variable
        # if it's set or "https://us.infisical.com".
        self.url = ... 
        
```

The you can add it to the provider chain and pass the provider chain to the client:

```python
from infisical.clients import InfisicalClient
from infisical.credentials.providers import InfisicalCredentialProviderChain
from my_provider import MyProvider

provider_chain = InfisicalCredentialProviderChain()
# You can change the index where it's inserted into the chain, but the default is 0.
provider_chain.add_provider(MyProvider(), 0)
client = InfisicalClient(provider_chain=provider_chain)
```

## Contributing

To have your PR accepted, ensure that you follow these guidelines. In a nutshell, here's what's required:

1) It passes `lint` and `test`, and it can `package` successfully.
2) You have updated the version in accordance with the [versioning](#versioning) guide.
3) Any changes or additions have [updated docs](#generate-documentation).

### Getting Started 

Ensure you have Python 3.11 or greater installed.

This repository builds with [pants](https://www.pantsbuild.org/), which only supports Linux and Mac. If you're on Windows, you can use WSL. To install pants, use this command:

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://static.pantsbuild.org/setup/get-pants.sh | bash
```

You can also use `brew` on Mac:

```zsh
brew install pantsbuild/tap/pants
```

Then you need to install the dependencies into a virtual environment. Do this by running:

```bash
pants venv
```

>NOTE: The `venv` command is just an alias. You can see the actual command in the `pants.toml` and read more about it [here](https://www.pantsbuild.org/2.25/docs/using-pants/setting-up-an-ide#python-third-party-dependencies-and-tools).

Then you can point your IDE's interpreter path to `dist/export/python/virtualenvs/python-default/<VERSION>/bin/python3`. In VSCode, it will pick up the dependencies symlinked in the venv and work just like a standard venv.

### Adding or Updating Dependencies

The project dependencies are pinned to the full semantic versions, which means they must be upgraded explicitly. This is to prevent accidental breaking changes deploying to production. Updating them is simple:

1) Update the desired dependency version in `project.dependencies` in the `pyproject.toml`.
2) Run `pants lock` to update the lock file.
3) Run `pants venv` to update the venv with the latest dependencies
4) Run `pants lint all`, `pants test all`, and `pants package all`. Make sure they all succeed.

>NOTE: All `project.optional-dependencies.dev` are pinned to the minor version, which means patch version are updated automatically during `pants lock` if a new version exists. 

### Lint, Test, and Build

To lint the project sources, just run

```bash
pants lint all
```

>NOTE: The `all` argument is just an alias for `::` in pants, which means all targets. I use this alias as it makes things a bit easier to understand.

If you run into any formatting or linting errors caught by [ruff](https://docs.astral.sh/ruff/), you can fix what is automatically fixable via

```bash
pants fix all
```

Anything else will have to be fixed by hand.

If all sources pass linting, you can run unit tests via:

```bash
pants test all
```

The test coverage will print to the console.

To make sure it builds after all tests pass, run:

```bash
pants package all
```

It will generate both a `*.whl` and a `*.tar.gz` in the `./dist` directory.

>NOTE: Ensure all three (lint, test, and build) pass before submitting a PR.

### Generate Documentation

To make it easier to generate API documentation, this repo automatically generates all documentation with MkDocs. So, all you have to do is make sure the class/method docstrings are updated correctly and run:

```bash
pants run mkdocs serve
```

This generates the markdown docs on-the-fly and serves them. You can then update the sources to see how it looks before committing, including the `stylesheet.css` and `README.md`. To check the fully built HTML files, just run:

```bash
pants run mkdocs build
```

It's not necessary, as the `serve` command runs the same code just without emitting the files.

>NOTE: It will generate the fully built HTML documentation in the `site` folder. The `docs` folder is necessary for MkDocs to populate the virtual Markdown files but they're not actually rendered out.

### Versioning

I like explicit semantic versioning, so if your PR is a patch or bug fix, increase the PATCH version by 1 in the `pyproject.toml`.

>EXAMPLE: If the current version is `1.0.0`, the version in your PR should be `1.0.1`.

If your PR introduces a new feature like implementing new or updated API routes, increase the MINOR version by 1 and set the PATCH version to 0.

>EXAMPLE: Version `1.0.1` now becomes `1.1.0`.

And any major or breaking changes, including things like refactoring, get their own MAJOR version release. This ensures those who pin the major version won't break in production, but can still get minor and patch updates.

### Deprecated API Routes

Infisical is known to deprecate certain API version routes. Should this be the case, the specified versioned route will raise a `DeprecationWarning` every call and we'll try to include deprecation messages specific to it, but we may continue to include the deprecated route until a major version release. That means, depending on your Infisical instance version may not contain routes in this SDK. In which case, the HTTP client will most likely return a `400` or `404`.

>NOTE: The parity between this SDK and Infisical's actual API will try to be as close as possible while still retaining backwards compatibility for those who have organizations that slow to upgrade.
