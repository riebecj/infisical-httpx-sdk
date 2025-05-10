"""Infisical Certificate Resource API."""

from typing import Final, Unpack

from infisical._types import SyncOrAsyncClient
from infisical.resources.base import InfisicalAPI

from .models import (
    Certificate,
    CertificateBodyChain,
    CertificateBundle,
    CertificatesList,
    IssueCertificateRequest,
    IssuedCertificate,
    ListCertificatesQueryParams,
    Revocation,
    RevocationReasons,
    SignCertificateRequest,
    SignedCertificate,
)


class CertificatesV1(InfisicalAPI):
    """Infisical Certificates v1 API Resource."""

    base_uri: Final = "/v1/pki/certificates"

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Certificates Resource."""
        super().__init__(client=client)

    def delete(self, *, serial_number: str) -> Certificate:
        """Delete a certificate."""
        self.logger.info("Deleting certificate %s", serial_number)
        url = self._format_url(f"/{serial_number}")
        request = self.client.create_request(method="delete", url=url)
        return self.client.handle_request(request=request, expected_responses={"certificate": Certificate})

    def get_certificate_body_chain(self, *, serial_number: str) -> CertificateBodyChain:
        """Get the certificate body and chain."""
        self.logger.info("Getting certificate body and chain for %s", serial_number)
        url = self._format_url(f"/{serial_number}/certificate")
        request = self.client.create_request(method="get", url=url)
        return self.client.handle_request(request=request, expected_responses={"": CertificateBodyChain})

    def get_certificate_bundle(self, *, serial_number: str) -> CertificateBundle:
        """Get the certificate bundle."""
        self.logger.info("Getting certificate bundle for %s", serial_number)
        url = self._format_url(f"/{serial_number}/bundle")
        request = self.client.create_request(method="get", url=url)
        return self.client.handle_request(request=request, expected_responses={"": CertificateBundle})

    def get_certificate_private_key(self, *, serial_number: str) -> str:
        """Get the certificate private key."""
        self.logger.info("Getting certificate private key for %s", serial_number)
        url = self._format_url(f"/{serial_number}/private-key")
        request = self.client.create_request(method="get", url=url)
        return self.client.handle_request(request=request, expected_responses={"": str})

    def issue_certificate(self, request: IssueCertificateRequest) -> IssuedCertificate:
        """Issue a new certificate."""
        self.logger.info("Issuing certificate %s", request.common_name)
        url = self._format_url("/issue-certificate")
        _request = self.client.create_request(
            method="post",
            url=url,
            body=request.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(request=_request, expected_responses={"certificate": IssuedCertificate})

    def revoke(self, *, serial_number: str, reason: RevocationReasons) -> Revocation:
        """Revoke a certificate."""
        self.logger.info("Revoking certificate: %s", serial_number)
        url = self._format_url(f"/{serial_number}/revoke")
        request = self.client.create_request(method="post", url=url, body={"revocationReason": reason})
        return self.client.handle_request(request=request, expected_responses={"": Revocation})

    def sign_certificate(self, csr: SignCertificateRequest) -> SignedCertificate:
        """Sign a certificate."""
        self.logger.info("Signing certificate: %s", csr.friendly_name or csr.common_name or "CSR")
        url = self._format_url("/sign-certificate")
        request = self.client.create_request(
            method="post",
            url=url,
            body=csr.model_dump(by_alias=True, exclude_none=True),
        )
        return self.client.handle_request(request=request, expected_responses={"certificate": SignedCertificate})


class CertificatesV2(InfisicalAPI):
    """Infisical Certificates v2 API Resource."""

    base_uri: Final = "/v2/workspace"

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Certificates Resource."""
        super().__init__(client=client)

    def list(self, *, slug: str, **params: Unpack[ListCertificatesQueryParams]) -> CertificatesList:
        """List all certificates in the specified project slug."""
        if "offset" in params and (params["offset"] < 0 or params["offset"] > 100):  # noqa: PLR2004
            self.raise_resource_error("Offset must be between 0 and 100.")
        if "limit" in params and (params["limit"] < 1 or params["limit"] > 100):  # noqa: PLR2004
            self.raise_resource_error("Limit must be between 1 and 100.")
        self.logger.info("Listing certificates in project %s", slug)
        request = self.client.create_request(
            method="get",
            url=self._format_url(f"/{slug}/certificates"),
            params=params,
        )
        return self.client.handle_request(request=request, expected_responses={"": CertificatesList})


class Certificates:
    """Infisical Certificates Resource."""

    def __init__(self, client: SyncOrAsyncClient) -> None:
        """Initialize the Infisical Certificates Resource."""
        self.v1 = CertificatesV1(client=client)
        self.v2 = CertificatesV2(client=client)
