import os
import ssl

import certifi


def default_ssl_context() -> ssl.SSLContext | bool:
    """Create a default SSL context.
    
    If the `INFISICAL_VERIFY_SSL` environment variable is set to `false`, `0`, or `no`, it will disable
    SSL verification for all clients. Otherwise, it will create a default SSL context using the
    `SSL_CERT_FILE` and/or `SSL_CERT_DIR` environment variables, or the default `certifi` certificate bundle.
    """
    if os.getenv("INFISICAL_VERIFY_SSL", "true").lower() not in ("0", "false", "no"):
        return ssl.create_default_context(
            cafile=os.environ.get("SSL_CERT_FILE", certifi.where()),
            capath=os.environ.get("SSL_CERT_DIR"),
        )
    return False
