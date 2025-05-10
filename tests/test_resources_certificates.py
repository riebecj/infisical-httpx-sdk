import datetime
import pytest

from infisical.exceptions import InfisicalResourceError
from infisical.resources.certificates.api import Certificates, CertificatesV1, CertificatesV2
from infisical.resources.certificates.models import Certificate, CertificateBodyChain, CertificateBundle, CertificatesList, IssueCertificateRequest, IssuedCertificate, Revocation, SignCertificateRequest, SignedCertificate


class TestCertificatesV1:

    def test_delete(self, mock_client, format_url):
        mock_client.handle_request.return_value = Certificate(
            id="id",
            caCertId="ca_cert_id",
            caId="ca_id",
            commonName="common_name",
            createdAt=datetime.datetime.now(),
            friendlyName="friendly_name",
            notAfter=datetime.datetime.now(),
            notBefore=datetime.datetime.now(),
            serialNumber="serial_number",
            status="status",
            updatedAt=datetime.datetime.now(),
        )

        serial_number = "test_serial_number"
        assert isinstance(
            CertificatesV1(client=mock_client).delete(serial_number=serial_number),
            Certificate
        )
        mock_client.create_request.assert_called_once_with(
            method="delete",
            url=format_url(CertificatesV1, f"/{serial_number}"),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"certificate": Certificate},
        )

    def test_get_certificate_body_chain(self, mock_client, format_url):
        mock_client.handle_request.return_value = CertificateBodyChain(
            certificate="certificate",
            certificateChain="certificate_chain",
            serialNumber="serial_number",
        )

        serial_number = "test_serial_number"
        assert isinstance(
            CertificatesV1(client=mock_client).get_certificate_body_chain(serial_number=serial_number),
            CertificateBodyChain
        )
        mock_client.create_request.assert_called_once_with(
            method="get",
            url=format_url(CertificatesV1, f"/{serial_number}/certificate"),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"": CertificateBodyChain},
        )

    def test_get_certificate_bundle(self, mock_client, format_url):
        mock_client.handle_request.return_value = CertificateBundle(
            certificate="certificate",
            certificateChain="certificate_chain",
            privateKey="private_key",
            serialNumber="serial_number",
        )

        serial_number = "test_serial_number"
        assert isinstance(
            CertificatesV1(client=mock_client).get_certificate_bundle(serial_number=serial_number),
            CertificateBundle
        )
        mock_client.create_request.assert_called_once_with(
            method="get",
            url=format_url(CertificatesV1, f"/{serial_number}/bundle"),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"": CertificateBundle},
        )

    def test_get_certificate_private_key(self, mock_client, format_url):
        mock_client.handle_request.return_value = "private_key"
        serial_number = "test_serial_number"
        assert CertificatesV1(client=mock_client).get_certificate_private_key(serial_number=serial_number) == "private_key"
        mock_client.create_request.assert_called_once_with(
            method="get",
            url=format_url(CertificatesV1, f"/{serial_number}/private-key"),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"": str},
        )

    def test_issue_certificate(self, mock_client, format_url):
        mock_client.handle_request.return_value = IssuedCertificate(
            certificate="certificate",
            certificateChain="certificate_chain",
            issuingCACertificate="issuing_ca_certificate",
            serialNumber="serial_number",
            privateKey="private_key",
        )

        test_request = IssueCertificateRequest(
            ca_id="ca_id",
            common_name="common_name",
            friendly_name="friendly_name",
            not_after=datetime.datetime.now(),
            not_before=datetime.datetime.now(),
            ttl="1h",
            workspace_id="test_workspace",
            environment="test_env",
        )
        assert isinstance(CertificatesV1(client=mock_client).issue_certificate(test_request), IssuedCertificate)
        mock_client.create_request.assert_called_once_with(
            method="post",
            url=format_url(CertificatesV1, "/issue-certificate"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"certificate": IssuedCertificate},
        )

    def test_revoke(self, mock_client, format_url):
        mock_client.handle_request.return_value = Revocation(
            message="revocation_message",
            revokedAt=datetime.datetime.now(),
            serialNumber="serial_number",
        )

        serial_number = "test_serial_number"
        reason = "UNSPECIFIED"
        assert isinstance(
            CertificatesV1(client=mock_client).revoke(serial_number=serial_number, reason=reason),
            Revocation
        )
        mock_client.create_request.assert_called_once_with(
            method="post",
            url=format_url(CertificatesV1, f"/{serial_number}/revoke"),
            body={"revocationReason": reason},
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"": Revocation},
        )

    def test_sign_certificate(self, mock_client, format_url):
        mock_client.handle_request.return_value = SignedCertificate(
            certificate="certificate",
            certificateChain="certificate_chain",
            issuingCACertificate="issuing_ca_certificate",
            serialNumber="serial_number",
        )

        test_request = SignCertificateRequest(
            ca_id="ca_id",
            common_name="common_name",
            csr="csr",
            friendly_name="friendly_name",
            ttl="1h",
            workspace_id="test_workspace",
            environment="test_env",
        )
        assert isinstance(CertificatesV1(client=mock_client).sign_certificate(test_request), SignedCertificate)
        mock_client.create_request.assert_called_once_with(
            method="post",
            url=format_url(CertificatesV1, "/sign-certificate"),
            body=test_request.model_dump(by_alias=True, exclude_none=True),
        )
        mock_client.handle_request.assert_called_once_with(
            request=mock_client.create_request.return_value,
            expected_responses={"certificate": SignedCertificate},
        )


class TestCertificatesV2:
    @pytest.mark.parametrize("params,exception", [
        ({"offset": -1}, InfisicalResourceError),
        ({"offset": 101}, InfisicalResourceError),
        ({"limit": 0}, InfisicalResourceError),
        ({"limit": 101}, InfisicalResourceError),
        ({"offset": 0, "limit": 1}, None),
        ({"offset": 100, "limit": 100}, None),
    ])
    def test_list(self, params, exception, mock_client, format_url):
        mock_client.handle_request.return_value = CertificatesList(
            certificates=[
                Certificate(
                    id="id",
                    caCertId="ca_cert_id",
                    caId="ca_id",
                    commonName="common_name",
                    createdAt=datetime.datetime.now(),
                    friendlyName="friendly_name",
                    notAfter=datetime.datetime.now(),
                    notBefore=datetime.datetime.now(),
                    serialNumber="serial_number",
                    status="status",
                    updatedAt=datetime.datetime.now(),
                )
            ]
        )

        slug = "test_slug"
        if exception:
            with pytest.raises(exception):
                CertificatesV2(client=mock_client).list(slug=slug, **params)
            mock_client.create_request.assert_not_called()
            mock_client.handle_request.assert_not_called()
        else:
            assert isinstance(CertificatesV2(client=mock_client).list(slug=slug, **params), CertificatesList)
            mock_client.create_request.assert_called_once_with(
                method="get",
                url=format_url(CertificatesV2, f"/{slug}/certificates"),
                params=params,
            )
            mock_client.handle_request.assert_called_once_with(
                request=mock_client.create_request.return_value,
                expected_responses={"": CertificatesList},
            )


class TestCertificates:
    def test_init(self, mock_client):
        certificates = Certificates(client=mock_client)
        assert isinstance(certificates.v1, CertificatesV1)
        assert isinstance(certificates.v2, CertificatesV2)
        assert certificates.v1.client == mock_client
        assert certificates.v2.client == mock_client
