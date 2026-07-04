# PKI X.509 Lab - Certificate Management System

A comprehensive Python-based Public Key Infrastructure (PKI) implementation for managing X.509 certificates using the cryptography library. This project provides a complete Certificate Authority (CA) infrastructure with support for certificate issuance, validation, revocation, and Certificate Revocation List (CRL) management.

## Overview

This PKI lab implements a three-tier certificate management system with the following components:

- **Certificate Authority (CA)**: Root CA for issuing and signing certificates
- **Registration Authority (RA)**: Validates certificate requests and manages approvals
- **Certificate Management**: Full lifecycle management of digital certificates

## Features

✅ **Certificate Authority Creation**
- Root CA generation with RSA-3072 encryption
- X.509 v3 certificate support with extensions
- Self-signed CA configuration

✅ **Certificate Signing Requests (CSR)**
- RSA-2048 key pair generation
- CSR creation for both client and server certificates
- Subject Alternative Names (SAN) support for DNS

✅ **Registration Authority (RA)**
- CSR validation and signature verification
- Identity database management
- Certificate type validation
- Approval workflow

✅ **Certificate Issuance**
- CA signing of approved requests
- Extended Key Usage (EKU) support
- Certificate serial number management
- Validity period configuration

✅ **Certificate Revocation**
- Revocation tracking with JSON storage
- Revocation reason specification
- CRL (Certificate Revocation List) generation
- CRL distribution points in certificates

✅ **Cryptographic Operations**
- RSA signature verification
- PEM format support
- SHA-256 hashing
- PKCS1v15 padding

## Directory Structure

```
pki/
├── ca/                   # CA private keys and certificates
├── keys/                 # Private keys for issued certificates
├── certs/                # Issued end-entity certificates
├── requests/             # Certificate Signing Requests
├── approvals/            # RA approval records (JSON)
└── crl/                  # Certificate Revocation Lists
    └── revocations.json  # Revocation tracking
```

## Installation

### Requirements
- Python 3.8+
- cryptography >= 42.0.0

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd PKI_X.509
```

2. Install dependencies:
```bash
pip install cryptography
```

3. Verify installation:
```bash
python pki_lab.py --help
```

## Usage

### Initialize Certificate Authority

```bash
python pki_lab.py create-ca
```

Creates the root CA with:
- 10-year validity period
- RSA-3072 key pair
- Basic constraints marked as critical

### Create Certificate Signing Request

```bash
python pki_lab.py create-csr --name client1 --type client
python pki_lab.py create-csr --name localhost --type server
```

Generates:
- Private key (pki/keys/)
- CSR file (pki/requests/)

### RA Approval Process

```bash
python pki_lab.py ra-approve \
    --csr pki/requests/client1.csr.pem \
    --requester-id client1 \
    --type client
```

Validates and creates approval record in JSON format.

### Sign Certificate

```bash
python pki_lab.py ca-sign \
    --approval pki/approvals/client1.approval.json \
    --days 365
```

Issues signed certificate to (pki/certs/).

### Revoke Certificate

```bash
python pki_lab.py revoke-cert \
    --cert pki/certs/client1.cert.pem \
    --reason key_compromise
```

Revocation reasons supported:
- `key_compromise`
- `ca_compromise`
- `affiliation_changed`
- `superseded`
- `cessation_of_operation`
- `certificate_hold`

### Verify Certificate

```bash
python pki_lab.py verify-cert \
    --cert pki/certs/client1.cert.pem
```

### Generate CRL

```bash
python pki_lab.py issue-crl
```

Generates updated Certificate Revocation List.

### Reset Lab

```bash
python pki_lab.py reset-demo
```

Cleans up all generated certificates and keys.

## Configuration

### Valid Identities

The system comes with two pre-configured identities:

```python
VALID_IDENTITIES = {
    "client1": {"cn": "client1", "type": "client"},
    "localhost": {"cn": "localhost", "type": "server"},
}
```

These can be extended in the code to support additional identities.

### Certificate Parameters

- **CA Key Size**: RSA-3072 (default)
- **End-Entity Key Size**: RSA-2048 (default)
- **Hash Algorithm**: SHA-256
- **CA Validity**: 10 years
- **Certificate Validity**: 1 year (default, configurable)
- **CRL Validity**: 7 days

## Workflow Example

```bash
# 1. Initialize CA
python pki_lab.py create-ca

# 2. Create CSR for client
python pki_lab.py create-csr --name client1 --type client

# 3. RA approves request
python pki_lab.py ra-approve \
    --csr pki/requests/client1.csr.pem \
    --requester-id client1 \
    --type client

# 4. CA signs certificate
python pki_lab.py ca-sign \
    --approval pki/approvals/client1.approval.json

# 5. Verify certificate
python pki_lab.py verify-cert \
    --cert pki/certs/client1.cert.pem

# 6. Later: Revoke if needed
python pki_lab.py revoke-cert \
    --cert pki/certs/client1.cert.pem

# 7. Update CRL
python pki_lab.py issue-crl
```

## Technical Details

### X.509 Extensions Implemented

**CA Certificate:**
- Basic Constraints (critical)
- Key Usage (critical)
- Subject Key Identifier

**End-Entity Certificate:**
- Basic Constraints
- Key Usage (KEU for server, DSU for client)
- Subject Key Identifier
- Authority Key Identifier
- CRL Distribution Points
- Extended Key Usage (EKU)
- Subject Alternative Names (SAN)

### Security Considerations

⚠️ **Development Lab Only**: This implementation is designed for educational purposes. For production use:
- Use hardware security modules (HSM) for key storage
- Implement proper access controls
- Use strong passwords for private keys
- Deploy across trusted infrastructure
- Implement audit logging
- Use secure communication channels

## Testing

Run basic operations:
```bash
python pki_lab.py create-ca
python pki_lab.py create-csr --name client1 --type client
python pki_lab.py ra-approve --csr pki/requests/client1.csr.pem --requester-id client1 --type client
python pki_lab.py ca-sign --approval pki/approvals/client1.approval.json
python pki_lab.py verify-cert --cert pki/certs/client1.cert.pem
```




## References

- [RFC 5280: X.509 PKI Certificate and CRL Profile](https://tools.ietf.org/html/rfc5280)
- [RFC 2986: PKCS #10](https://tools.ietf.org/html/rfc2986)
- [Cryptography Library Documentation](https://cryptography.io)
- [OpenSSL Command Line Tools](https://www.openssl.org)

---

