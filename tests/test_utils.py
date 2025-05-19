import ssl
import pytest
import os

from infisical.utils import default_ssl_context


class TestUtilities:
    @pytest.mark.parametrize("env_setting", ["false", "0", "no", None])
    def test_default_ssl_context(self, env_setting):
        if env_setting:
            os.environ["INFISICAL_VERIFY_SSL"] = env_setting
            assert not default_ssl_context()
        else:
            os.environ.pop("INFISICAL_VERIFY_SSL")
            assert isinstance(default_ssl_context(), ssl.SSLContext)
