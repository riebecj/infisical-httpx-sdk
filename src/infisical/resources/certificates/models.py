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
    """Query parameters for listing certificates."""

    commonName: str
    friendlyName: str
    limit: int
    offset: int


class Certificate(BaseModel):
    """Certificate model."""

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
    """Certificates list model."""

    certificates: Annotated[list[Certificate], Field(alias="certificates")]


class CertificateBodyChain(BaseModel):
    """Certificate body and chain model."""

    certificate_chain: Annotated[str | None, Field(alias="certificateChain", default=None)]
    certificate: Annotated[str, Field()]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class CertificateBundle(BaseModel):
    """Certificate bundle model."""

    certificate_chain: Annotated[str | None, Field(alias="certificateChain", default=None)]
    certificate: Annotated[str, Field()]
    private_key: Annotated[str, Field(alias="privateKey")]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class Revocation(BaseModel):
    """Revocation model."""

    message: Annotated[str, Field()]
    revoked_at: Annotated[datetime.datetime, Field(alias="revokedAt")]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class IssueCertificateRequest(InfisicalResourceRequest):
    """Issue certificate request model."""

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
    """Sign certificate request model."""

    alt_names: Annotated[list[str] | None, Field(alias="altNames", default=None)]
    ca_id: Annotated[str, Field(alias="caId")]
    certificate_template_id: Annotated[str | None, Field(alias="certificateTemplateId", default=None)]
    common_name: Annotated[str, Field(alias="commonName")]
    csr: Annotated[str, Field(alias="csr")]
    extended_key_usages: Annotated[list[ExtendedKeyUsages] | None, Field(alias="extendedKeyUsages", default=None)]
    friendly_name: Annotated[str, Field(alias="friendlyName")]
    key_usages: Annotated[list[KeyUsages] | None, Field(alias="keyUsages", default=None)]
    not_after: Annotated[datetime.datetime | None, Field(alias="notAfter", default=None)]
    not_before: Annotated[datetime.datetime | None, Field(alias="notBefore", default=None)]
    pki_collection_id: Annotated[str | None, Field(alias="pkiCollectionId", default=None)]
    ttl: Annotated[str, Field(alias="ttl")]


class SignedCertificate(BaseModel):
    """Signed certificate model."""

    certificate_chain: Annotated[str, Field(alias="certificateChain")]
    certificate: Annotated[str, Field()]
    issuing_ca_certificate: Annotated[str, Field(alias="issuingCACertificate")]
    serial_number: Annotated[str, Field(alias="serialNumber")]


class IssuedCertificate(SignedCertificate):
    """Issued certificate model."""

    private_key: Annotated[str, Field(alias="privateKey")]
