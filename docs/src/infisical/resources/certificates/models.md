# Models

[Infisical HTTPX SDK Documentation](../../../../README.md#infisical-httpx-sdk-documentation) / `src` / [Infisical](../../index.md#infisical) / [Resources](../index.md#resources) / [Certificates](./index.md#certificates) / Models

> Auto-generated documentation for [src.infisical.resources.certificates.models](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py) module.

- [Models](#models)
  - [Certificate](#certificate)
  - [CertificateBodyChain](#certificatebodychain)
  - [CertificateBundle](#certificatebundle)
  - [CertificatesList](#certificateslist)
  - [IssueCertificateRequest](#issuecertificaterequest)
  - [IssuedCertificate](#issuedcertificate)
  - [ListCertificatesQueryParams](#listcertificatesqueryparams)
  - [Revocation](#revocation)
  - [SignCertificateRequest](#signcertificaterequest)
  - [SignedCertificate](#signedcertificate)

## Certificate

[Show source in models.py:51](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L51)

Certificate model.

#### Signature

```python
class Certificate(BaseModel): ...
```



## CertificateBodyChain

[Show source in models.py:79](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L79)

Certificate body and chain model.

#### Signature

```python
class CertificateBodyChain(BaseModel): ...
```



## CertificateBundle

[Show source in models.py:87](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L87)

Certificate bundle model.

#### Signature

```python
class CertificateBundle(BaseModel): ...
```



## CertificatesList

[Show source in models.py:73](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L73)

Certificates list model.

#### Signature

```python
class CertificatesList(BaseModel): ...
```



## IssueCertificateRequest

[Show source in models.py:104](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L104)

Issue certificate request model.

#### Signature

```python
class IssueCertificateRequest(InfisicalResourceRequest): ...
```



## IssuedCertificate

[Show source in models.py:146](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L146)

Issued certificate model.

#### Signature

```python
class IssuedCertificate(SignedCertificate): ...
```

#### See also

- [SignedCertificate](#signedcertificate)



## ListCertificatesQueryParams

[Show source in models.py:42](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L42)

Query parameters for listing certificates.

#### Signature

```python
class ListCertificatesQueryParams(TypedDict): ...
```



## Revocation

[Show source in models.py:96](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L96)

Revocation model.

#### Signature

```python
class Revocation(BaseModel): ...
```



## SignCertificateRequest

[Show source in models.py:120](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L120)

Sign certificate request model.

#### Signature

```python
class SignCertificateRequest(InfisicalResourceRequest): ...
```



## SignedCertificate

[Show source in models.py:137](https://github.com/riebecj/infisical-httpx-sdk/blob/main/src/infisical/resources/certificates/models.py#L137)

Signed certificate model.

#### Signature

```python
class SignedCertificate(BaseModel): ...
```