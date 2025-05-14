"""Infisical Certificate Resource Models."""

import datetime
from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, Field

from infisical.resources.base import InfisicalResourceRequest

ExtendedKeyUsages = Literal[
    "clientAuth",
    "codeSigning",
    "emailProtection",
    "ocspSigning",
    "serverAuth",
    "timeStamping",
]
KeyUsages = Literal[
    "cRLSign",
    "dataEncipherment",
    "decipherOnly",
    "digitalSignature",
    "encipherOnly",
    "keyAgreement",
    "keyCertSign",
    "keyEncipherment",
    "nonRepudiation",
]
RevocationReasons = Literal[
    "A_A_COMPROMISE",
    "AFFILIATION_CHANGED",
    "CA_COMPROMISE",
    "CERTIFICATE_HOLD",
    "CESSATION_OF_OPERATION",
    "KEY_COMPROMISE",
    "PRIVILEGE_WITHDRAWN",
    "SUPERSEDED",
    "UNSPECIFIED",
]


class ListCertificatesQueryParams(TypedDict, total=False):
    """Query parameters for listing certificates.

    Theese the available query parameters you can pass to the
    [list][src.infisical.resources.certificates.api.CertificatesV2.] method.

    Other parameters:
        limit (int): The maximum number of certificates to return, between `1` and `100` inclusive.
        offset (int): The offset for pagination, between `0` and `100` inclusive.
        commonName (str): The common name of the certificate.
        friendlyName (str): The friendly name of the certificate.
    """

    commonName: str
    friendlyName: str
    limit: int
    offset: int


class Certificate(BaseModel):
    """Certificate model.

    Attributes:
        alt_names (list[str] | str | None): Alternative names for the certificate.
        ca_cert_id (str): The ID of the CA certificate.
        ca_id (str): The ID of the CA.
        certificate_id (str): The ID of the certificate.
        certificate_template_id (str | None): The ID of the certificate template.
        common_name (str): The common name for the certificate.
        created_at (datetime.datetime): The creation date of the certificate.
        extended_key_usages (list[str] | None): Extended key usages for the certificate.
        friendly_name (str): A friendly name for the certificate.
        key_usages (list[str] | None): Key usages for the certificate.
        not_after (datetime.datetime): The expiration date of the certificate.
        not_before (datetime.datetime): The start date of the certificate's validity period.
        revocation_reason (int | None): The reason for revocation, if applicable.
        revoked_at (datetime.datetime | None): The date when the certificate was revoked, if applicable.
        serial_number (str): The serial number of the certificate.
        status (str): The status of the certificate.
        updated_at (datetime.datetime): The last update date of the certificate.
    """

    alt_names: Annotated[list[str] | str | None, Field(alias="altNames", default=None)]
    ca_cert_id: Annotated[str, Field(alias="caCertId")]
    ca_id: Annotated[str, Field(alias="caId")]
    certificate_id: Annotated[str, Field(alias="id")]
    certificate_template_id: Annotated[str | None, Field(alias="certificateTemplateId", default=None)]
    common_name: Annotated[str, Field(alias="commonName")]
    created_at: Annotated[datetime.datetime, Field(alias="createdAt")]
    extended_key_usages: Annotated[list[str] | None, Field(alias="extendedKeyUsages", default=None)]
    friendly_name: Annotated[str, Field(alias="friendlyName")]
    key_usages: Annotated[list[str] | None, Field(alias="keyUsages", default=None)]
    not_after: Annotated[datetime.datetime, Field(alias="notAfter")]
    not_before: Annotated[datetime.datetime, Field(alias="notBefore")]
    revocation_reason: Annotated[int | None, Field(alias="revocationReason", default=None)]
    revoked_at: Annotated[datetime.datetime | None, Field(alias="revokedAt", default=None)]
    serial_number: Annotated[str, Field(alias="serialNumber")]
    status: Annotated[str, Field()]
    updated_at: Annotated[datetime.datetime, Field(alias="updatedAt")]


class CertificatesList(BaseModel):
    """Certificates list model.

    Attributes:
        certificates (list[Certificate]): A list of certificates.
    """

    certificates: Annotated[list[Certificate], Field(alias="certificates")]


class CertificateBodyChain(BaseModel):
    """Certificate body and chain model.

    Attributes:
        certificate_chain (str | None): The certificate chain.
        certificate (str): The certificate.
        serial_number (str): The serial number of the certificate.
    """

    certificate_chain: Annotated[str | None, Field(alias="certificateChain", default=None)]
    certificate: Annotated[str, Field()]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class CertificateBundle(BaseModel):
    """Certificate bundle model.

    Attributes:
        certificate_chain (str | None): The certificate chain.
        certificate (str): The certificate.
        private_key (str): The private key.
        serial_number (str): The serial number of the certificate.
    """

    certificate_chain: Annotated[str | None, Field(alias="certificateChain", default=None)]
    certificate: Annotated[str, Field()]
    private_key: Annotated[str, Field(alias="privateKey")]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class Revocation(BaseModel):
    """Revocation model.

    Attributes:
        message (str): The revocation message.
        revoked_at (datetime.datetime): The date when the certificate was revoked.
        serial_number (str): The serial number of the certificate.
    """

    message: Annotated[str, Field()]
    revoked_at: Annotated[datetime.datetime, Field(alias="revokedAt")]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class IssueCertificateRequest(InfisicalResourceRequest):
    """Issue certificate request model.

    The following are required when creating a new request:
        - `ca_id`
        - `common_name`
        - `friendly_name`
        - `ttl`
        - `workspace_id`
        - `environment`

    Attributes:
        alt_names (list[str] | None): Alternative names for the certificate.
        ca_id (str): The ID of the CA.
        certificate_template_id (str | None): The ID of the certificate template.
        common_name (str): The common name for the certificate.
        extended_key_usages (list[ExtendedKeyUsages] | None): Extended key usages for the certificate.
        friendly_name (str): A friendly name for the certificate.
        key_usages (list[KeyUsages] | None): Key usages for the certificate.
        not_after (datetime.datetime | None): The expiration date of the certificate.
        not_before (datetime.datetime | None): The start date of the certificate's validity period.
        pki_collection_id (str | None): The ID of the PKI collection.
        ttl (str): The time-to-live for the certificate.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment for the certificate.
    """

    alt_names: Annotated[list[str] | None, Field(alias="altNames", default=None)]
    ca_id: Annotated[str, Field(alias="caId")]
    certificate_template_id: Annotated[str | None, Field(alias="certificateTemplateId", default=None)]
    common_name: Annotated[str, Field(alias="commonName")]
    extended_key_usages: Annotated[list[ExtendedKeyUsages] | None, Field(alias="extendedKeyUsages", default=None)]
    friendly_name: Annotated[str, Field(alias="friendlyName")]
    key_usages: Annotated[list[KeyUsages] | None, Field(alias="keyUsages", default=None)]
    not_after: Annotated[datetime.datetime | None, Field(alias="notAfter", default=None)]
    not_before: Annotated[datetime.datetime | None, Field(alias="notBefore", default=None)]
    pki_collection_id: Annotated[str | None, Field(alias="pkiCollectionId", default=None)]
    ttl: Annotated[str, Field(alias="ttl")]


class SignCertificateRequest(InfisicalResourceRequest):
    """Sign certificate request model.

    The following are required when creating a new request:
        - `ca_id`
        - `common_name`
        - `csr`
        - `friendly_name`
        - `ttl`
        - `workspace_id`
        - `environment`

    Attributes:
        alt_names (list[str] | None): Alternative names for the certificate.
        ca_id (str): The ID of the CA.
        certificate_template_id (str | None): The ID of the certificate template.
        common_name (str): The common name for the certificate.
        csr (str): The Certificate Signing Request (CSR).
        extended_key_usages (list[ExtendedKeyUsages] | None): Extended key usages for the certificate.
        friendly_name (str): A friendly name for the certificate.
        key_usages (list[KeyUsages] | None): Key usages for the certificate.
        not_after (datetime.datetime | None): The expiration date of the certificate.
        not_before (datetime.datetime | None): The start date of the certificate's validity period.
        pki_collection_id (str | None): The ID of the PKI collection.
        ttl (str): The time-to-live for the certificate.
        workspace_id (str): The ID of the workspace.
        environment (str): The environment for the certificate.
    """

    alt_names: list[str] | None = Field(alias="altNames", default=None)
    ca_id: str = Field(alias="caId")
    certificate_template_id: str | None = Field(alias="certificateTemplateId", default=None)
    common_name: str = Field(alias="commonName")
    csr: str = Field(alias="csr")
    extended_key_usages: list[ExtendedKeyUsages] | None = Field(alias="extendedKeyUsages", default=None)
    friendly_name: str = Field(alias="friendlyName")
    key_usages: list[KeyUsages] | None = Field(alias="keyUsages", default=None)
    not_after: datetime.datetime | None = Field(alias="notAfter", default=None)
    not_before: datetime.datetime | None = Field(alias="notBefore", default=None)
    pki_collection_id: str | None = Field(alias="pkiCollectionId", default=None)
    ttl: str = Field(alias="ttl")


class SignedCertificate(BaseModel):
    """Signed certificate model.

    Attributes:
        certificate_chain (str): The certificate chain.
        certificate (str): The certificate.
        issuing_ca_certificate (str): The issuing CA certificate.
        serial_number (str): The serial number of the certificate.
    """

    certificate_chain: Annotated[str, Field(alias="certificateChain")]
    certificate: Annotated[str, Field()]
    issuing_ca_certificate: Annotated[str, Field(alias="issuingCACertificate")]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class IssuedCertificate(SignedCertificate):
    """Issued certificate model.

    It subclasses [SignedCertificate][(m).] because the attributes are the same
    except this one also returns the `private_key`.

    Attributes:
        certificate_chain (str): The certificate chain.
        certificate (str): The certificate.
        issuing_ca_certificate (str): The issuing CA certificate.
        private_key (str): The private key.
        serial_number (str): The serial number of the certificate.
    """

    private_key: Annotated[str, Field(alias="privateKey")]
