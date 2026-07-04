# Manual Git Commands - PKI X.509 Lab Setup

If you prefer to run git commands manually, or if the scripts don't work properly, use these commands:

## Step 0: Initialize Repository

```bash
cd C:\Users\Nine\Downloads\git\PKI_X.509

git init

# Configure your git identity (only first time)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Step 1: Core Infrastructure Commit

```bash
git add pki_lab.py
git commit -m "feat: initial project structure with core infrastructure

- Add main pki_lab.py module
- Define PKI directory structure (CA, keys, certs, CRL, approvals)
- Implement utility functions for file I/O (save_pem, load_private_key, etc.)
- Setup path constants for certificate storage
- Add VALID_IDENTITIES configuration for client and server types"
```

## Step 2: Certificate Authority Commit

```bash
git add pki_lab.py
git commit -m "feat: add Certificate Authority (CA) creation functionality

- Implement create_ca() function with RSA-3072 key generation
- Generate self-signed root CA certificate
- Set CA validity to 10 years
- Add X.509 v3 extensions (BasicConstraints, KeyUsage, SubjectKeyIdentifier)
- Configure CA for certificate signing and CRL generation"
```

## Step 3: CSR Generation Commit

```bash
git add pki_lab.py
git commit -m "feat: implement CSR generation with SAN support

- Add create_csr() function with RSA-2048 key generation
- Support client and server certificate types
- Implement Subject Alternative Names (SAN) for DNS entries
- Generate private keys and CSR files in PEM format
- Add identity validation for CSR generation"
```

## Step 4: RA Approval Workflow Commit

```bash
git add pki_lab.py
git commit -m "feat: add RA certificate request approval process

- Implement ra_approve() function for CSR validation
- Verify CSR signatures using RSA public key validation
- Validate identity against VALID_IDENTITIES database
- Enforce SAN requirements for server certificates
- Generate approval records in JSON format
- Add CSR subject CN validation matching requester identity"
```

## Step 5: CA Signing Functionality Commit

```bash
git add pki_lab.py
git commit -m "feat: implement certificate signing by CA

- Add ca_sign() function for issuing certificates
- Support configurable certificate validity periods (default 1 year)
- Implement X.509 v3 extensions for end-entity certificates
- Add Key Usage (KEU for server, DSU for client)
- Include Subject Key Identifier and Authority Key Identifier
- Configure CRL Distribution Points in issued certificates"
```

## Step 6: Extended Key Usage Features Commit

```bash
git add pki_lab.py
git commit -m "feat: implement Extended Key Usage and advanced certificate features

- Add ExtendedKeyUsage (EKU) for SERVER_AUTH and CLIENT_AUTH
- Preserve SAN extensions in issued certificates
- Implement KeyUsage flags for different certificate types
- Add support for multiple cryptographic algorithms
- Handle certificate attribute extraction (get_common_name function)
- Add RSA signature verification functionality"
```

## Step 7: Revocation and CRL Commit

```bash
git add pki_lab.py
git commit -m "feat: implement certificate revocation and CRL management

- Add revoke_certificate() function with revocation tracking
- Store revocations in JSON format with reason codes
- Implement issue_crl() for Certificate Revocation List generation
- Support multiple revocation reasons (key_compromise, superseded, etc.)
- Add CRL validity configuration (7 days default)
- Include revocation reason extensions in CRL entries"
```

## Step 8: Documentation Commit

```bash
git add README.md .gitignore
git commit -m "docs: add comprehensive README and project documentation

- Create detailed README with feature overview
- Document directory structure and usage workflows
- Add installation and setup instructions
- Include CLI usage examples for all operations
- Document X.509 extensions implemented
- Add security considerations and best practices
- Include RFC references and related documentation links
- Create .gitignore for Python and generated certificate files"
```

## Verify All Commits

After running all commands, verify the commits were created:

```bash
git log --oneline
```

You should see 8 commits listed.

## Push to GitHub

After creating a new repository on GitHub:

```bash
# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Rename branch to main (if needed)
git branch -M main

# Push all commits at once
git push -u origin main
```

## Troubleshooting

**If you get "CRLF will be converted to LF" warning:**
```bash
git config --global core.safecrlf true
```

**If you need to undo a commit (before pushing):**
```bash
git reset --soft HEAD~1
```

**To check git status:**
```bash
git status
```

**To see what changed:**
```bash
git diff
```

---

All 8 commits represent logical milestones in the PKI project development and showcase progressive feature implementation!
