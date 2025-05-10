# Api

[Infisical HTTPX SDK Documentation](../../README.md#infisical-httpx-sdk-documentation) / [Resources](../index.md#resources) / [Certificates](./index.md#certificates) / Api

> Auto-generated documentation for [resources.certificates.api](../../../src/infisical/resources/certificates/api.py) module.

## Certificates

[Show source in api.py:114](../../../src/infisical/resources/certificates/api.py#L114)

Infisical Certificates Resource.

#### Signature

```python
class Certificates:
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```



## CertificatesV1

[Show source in api.py:23](../../../src/infisical/resources/certificates/api.py#L23)

Infisical Certificates v1 API Resource.

#### Signature

```python
class CertificatesV1(InfisicalAPI):
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```

### CertificatesV1().delete

[Show source in api.py:32](../../../src/infisical/resources/certificates/api.py#L32)

Delete a certificate.

#### Signature

```python
def delete(self, serial_number: str) -> Certificate: ...
```

### CertificatesV1().get_certificate_body_chain

[Show source in api.py:39](../../../src/infisical/resources/certificates/api.py#L39)

Get the certificate body and chain.

#### Signature

```python
def get_certificate_body_chain(self, serial_number: str) -> CertificateBodyChain: ...
```

### CertificatesV1().get_certificate_bundle

[Show source in api.py:46](../../../src/infisical/resources/certificates/api.py#L46)

Get the certificate bundle.

#### Signature

```python
def get_certificate_bundle(self, serial_number: str) -> CertificateBundle: ...
```

### CertificatesV1().get_certificate_private_key

[Show source in api.py:53](../../../src/infisical/resources/certificates/api.py#L53)

Get the certificate private key.

#### Signature

```python
def get_certificate_private_key(self, serial_number: str) -> str: ...
```

### CertificatesV1().issue_certificate

[Show source in api.py:60](../../../src/infisical/resources/certificates/api.py#L60)

Issue a new certificate.

#### Signature

```python
def issue_certificate(self, request: IssueCertificateRequest) -> IssuedCertificate: ...
```

### CertificatesV1().revoke

[Show source in api.py:71](../../../src/infisical/resources/certificates/api.py#L71)

Revoke a certificate.

#### Signature

```python
def revoke(self, serial_number: str, reason: RevocationReasons) -> Revocation: ...
```

### CertificatesV1().sign_certificate

[Show source in api.py:78](../../../src/infisical/resources/certificates/api.py#L78)

Sign a certificate.

#### Signature

```python
def sign_certificate(self, csr: SignCertificateRequest) -> SignedCertificate: ...
```



## CertificatesV2

[Show source in api.py:90](../../../src/infisical/resources/certificates/api.py#L90)

Infisical Certificates v2 API Resource.

#### Signature

```python
class CertificatesV2(InfisicalAPI):
    def __init__(self, client: SyncOrAsyncClient) -> None: ...
```

### CertificatesV2().list

[Show source in api.py:99](../../../src/infisical/resources/certificates/api.py#L99)

List all certificates in the specified project slug.

#### Signature

```python
def list(
    self, slug: str, **params: Unpack[ListCertificatesQueryParams]
) -> CertificatesList: ...
```
