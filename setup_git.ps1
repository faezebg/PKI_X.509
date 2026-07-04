#!/usr/bin/env pwsh
# PKI X.509 Lab - Git Setup Script (PowerShell)
# This script initializes git and creates 8 meaningful commits

Set-Location $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PKI X.509 Lab - Git Repository Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configure git
Write-Host "[1/9] Initializing git repository..." -ForegroundColor Yellow
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
Write-Host ""

# Step 1: Initial commit
Write-Host "[2/9] Commit 1: Core infrastructure and utilities..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: initial project structure with core infrastructure

- Add main pki_lab.py module
- Define PKI directory structure (CA, keys, certs, CRL, approvals)
- Implement utility functions for file I/O (save_pem, load_private_key, etc.)
- Setup path constants for certificate storage
- Add VALID_IDENTITIES configuration for client and server types"
Write-Host ""

# Step 2: CA creation
Write-Host "[3/9] Commit 2: Implement Certificate Authority creation..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: add Certificate Authority (CA) creation functionality

- Implement create_ca() function with RSA-3072 key generation
- Generate self-signed root CA certificate
- Set CA validity to 10 years
- Add X.509 v3 extensions (BasicConstraints, KeyUsage, SubjectKeyIdentifier)
- Configure CA for certificate signing and CRL generation"
Write-Host ""

# Step 3: CSR generation
Write-Host "[4/9] Commit 3: Add Certificate Signing Request (CSR) generation..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: implement CSR generation with SAN support

- Add create_csr() function with RSA-2048 key generation
- Support client and server certificate types
- Implement Subject Alternative Names (SAN) for DNS entries
- Generate private keys and CSR files in PEM format
- Add identity validation for CSR generation"
Write-Host ""

# Step 4: RA approval
Write-Host "[5/9] Commit 4: Implement Registration Authority approval workflow..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: add RA certificate request approval process

- Implement ra_approve() function for CSR validation
- Verify CSR signatures using RSA public key validation
- Validate identity against VALID_IDENTITIES database
- Enforce SAN requirements for server certificates
- Generate approval records in JSON format
- Add CSR subject CN validation matching requester identity"
Write-Host ""

# Step 5: Certificate signing
Write-Host "[6/9] Commit 5: Add CA certificate signing functionality..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: implement certificate signing by CA

- Add ca_sign() function for issuing certificates
- Support configurable certificate validity periods (default 1 year)
- Implement X.509 v3 extensions for end-entity certificates
- Add Key Usage (KEU for server, DSU for client)
- Include Subject Key Identifier and Authority Key Identifier
- Configure CRL Distribution Points in issued certificates"
Write-Host ""

# Step 6: EKU and SAN
Write-Host "[7/9] Commit 6: Add Extended Key Usage and certificate features..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: implement Extended Key Usage and advanced certificate features

- Add ExtendedKeyUsage (EKU) for SERVER_AUTH and CLIENT_AUTH
- Preserve SAN extensions in issued certificates
- Implement KeyUsage flags for different certificate types
- Add support for multiple cryptographic algorithms
- Handle certificate attribute extraction (get_common_name function)
- Add RSA signature verification functionality"
Write-Host ""

# Step 7: Revocation and CRL
Write-Host "[8/9] Commit 7: Add certificate revocation and CRL management..." -ForegroundColor Yellow
git add pki_lab.py
git commit -m "feat: implement certificate revocation and CRL management

- Add revoke_certificate() function with revocation tracking
- Store revocations in JSON format with reason codes
- Implement issue_crl() for Certificate Revocation List generation
- Support multiple revocation reasons (key_compromise, superseded, etc.)
- Add CRL validity configuration (7 days default)
- Include revocation reason extensions in CRL entries"
Write-Host ""

# Step 8: Documentation
Write-Host "[9/9] Commit 8: Add comprehensive documentation..." -ForegroundColor Yellow
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
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Git repository setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your repository now contains 8 meaningful commits:" -ForegroundColor Yellow
Write-Host "  1. Initial project structure with core infrastructure"
Write-Host "  2. Certificate Authority creation"
Write-Host "  3. Certificate Signing Request generation"
Write-Host "  4. Registration Authority approval workflow"
Write-Host "  5. CA certificate signing functionality"
Write-Host "  6. Extended Key Usage and certificate features"
Write-Host "  7. Certificate revocation and CRL management"
Write-Host "  8. Documentation and configuration"
Write-Host ""
Write-Host "Next steps to push to GitHub:" -ForegroundColor Yellow
Write-Host "  1. Create a new repository on GitHub"
Write-Host "  2. Run the following commands:"
Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
Write-Host "     git branch -M main"
Write-Host "     git push -u origin main"
Write-Host ""
Write-Host "All commits will be pushed at once!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
