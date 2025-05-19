"""Infisical HTTPX SDK Utility Functions."""

import os
import ssl

import certifi


def default_ssl_context() -> ssl.SSLContext | bool:
    """Create a default SSL context.

    If the `INFISICAL_VERIFY_SSL` environment variable is set to `false`, `0`, or `no`, it will disable
    SSL verification for all clients. Otherwise, it will create a default SSL context using the optional
    `SSL_CERT_FILE` and/or `SSL_CERT_DIR` environment variables. Otherwise, the default `certifi` certificate
    bundle is used as the default cert file.

    ???+ tip

        If you're not doing anything with self-signed certificates, you can just use the default `certifi` certificate
        bundle. If you are using self-signed certificates, include the root and/or intermediate certificates in your
        OS's trust store and either set the `SSL_CERT_FILE` or `SSL_CERT_DIR` environment variables appropriately.

    Returns:
        (ssl.SSLContext): The SSL context to use for the HTTPX client.
        (bool): `False` if SSL verification is disabled.
    """
    if os.getenv("INFISICAL_VERIFY_SSL", "true").lower() not in ("0", "false", "no"):
        return ssl.create_default_context(
            cafile=os.environ.get("SSL_CERT_FILE", certifi.where()),
            capath=os.environ.get("SSL_CERT_DIR"),
        )
    return False
