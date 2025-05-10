import pytest

from infisical.resources.base import InfisicalAPI


class TestInfisicalAPI:
    def test_deprecation(self, mock_client):
        class TestResource(InfisicalAPI):
            base_uri = "/test"
            deprecated = True
            def __init__(self, client):
                super().__init__(client=client)
        
        with pytest.deprecated_call():
            TestResource(client=mock_client)._format_url(uri="test")
