import argparse
import base64
import datetime as dt
import json
import shutil
import socket
from pathlib import Path
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import (
    ExtendedKeyUsageOID,
    NameOID,
)
BASE = Path("pki")
CA_DIR = BASE / "ca"
REQ_DIR = BASE / "requests"
CERT_DIR = BASE / "certs"
CRL_DIR = BASE / "crl"
KEY_DIR = BASE / "keys"
APPROVAL_DIR = BASE / "approvals"
CA_KEY = CA_DIR / "ca.key.pem"
CA_CERT = CA_DIR / "ca.cert.pem"
CRL_FILE = CRL_DIR / "ca.crl.pem"
REVOCATIONS = CRL_DIR / "revocations.json"
VALID_IDENTITIES = {
    "client1": {"cn": "client1", "type": "client"},
    "localhost": {"cn": "localhost", "type": "server"},
}
def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)
def ensure_dirs():
    for d in [CA_DIR, REQ_DIR, CERT_DIR, CRL_DIR, KEY_DIR, APPROVAL_DIR]:
        d.mkdir(parents=True, exist_ok=True)
def save_pem(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
def load_private_key(path: Path):
    return serialization.load_pem_private_key(path.read_bytes(), password=None)
def load_cert(path: Path) -> x509.Certificate:
    return x509.load_pem_x509_certificate(path.read_bytes())
def load_csr(path: Path) -> x509.CertificateSigningRequest:
    return x509.load_pem_x509_csr(path.read_bytes())
def load_crl(path: Path) -> x509.CertificateRevocationList:
    return x509.load_pem_x509_crl(path.read_bytes())
def rsa_verify_signature(public_key, signature, signed_bytes, signature_hash_algorithm):
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("This lab script currently verifies only RSA keys.")
    public_key.verify(
        signature,
        signed_bytes,
        padding.PKCS1v15(),
        signature_hash_algorithm,
    )
def create_ca():
    ensure_dirs()
    if CA_KEY.exists() or CA_CERT.exists():
        raise FileExistsError("CA already exists. Delete pki/ first or run reset-demo.")
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PKI Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, "PKI Lab Root CA"),
    ])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now_utc() - dt.timedelta(minutes=5))
        .not_valid_after(now_utc() + dt.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )
    save_pem(
        CA_KEY,
        ca_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ),
    )
    save_pem(CA_CERT, ca_cert.public_bytes(serialization.Encoding.PEM))
    print(f"CA created:\n- {CA_KEY}\n- {CA_CERT}")
def create_csr(name: str, cert_type: str):
    ensure_dirs()
    if name not in VALID_IDENTITIES:
        raise ValueError(f"Unknown identity: {name}. Allowed: {list(VALID_IDENTITIES)}")
    if VALID_IDENTITIES[name]["type"] != cert_type:
        raise ValueError("Requested certificate type does not match registered identity.")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PKI Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, name),
    ])
    builder = x509.CertificateSigningRequestBuilder().subject_name(subject)
    if cert_type == "server":
        builder = builder.add_extension(
            x509.SubjectAlternativeName([x509.DNSName(name)]),
            critical=False
        )
    csr = builder.sign(key, hashes.SHA256())
    key_path = KEY_DIR / f"{name}.key.pem"
    csr_path = REQ_DIR / f"{name}.csr.pem"
    save_pem(
        key_path,
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ),
    )
    save_pem(csr_path, csr.public_bytes(serialization.Encoding.PEM))
    print(f"CSR created:\n- private key: {key_path}\n- csr: {csr_path}")
def get_common_name(name: x509.Name) -> str:
    attrs = name.get_attributes_for_oid(NameOID.COMMON_NAME)
    if not attrs:
        raise ValueError("Subject has no Common Name.")
    return attrs[0].value
def ra_approve(csr_path: Path, requester_id: str, cert_type: str):
    ensure_dirs()
    csr = load_csr(csr_path)
    if not csr.is_signature_valid:
        raise ValueError("CSR signature is invalid.")
    cn = get_common_name(csr.subject)
    expected = VALID_IDENTITIES.get(requester_id)
    if expected is None:
        raise ValueError("Requester is not registered in RA identity database.")
    if expected["cn"] != cn:
        raise ValueError("CSR Common Name does not match requester identity.")
    if expected["type"] != cert_type:
        raise ValueError("Requested certificate type does not match RA records.")
    if cert_type == "server":
        try:
            san = csr.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
            dns_names = san.get_values_for_type(x509.DNSName)
            if cn not in dns_names:
                raise ValueError("Server CSR must include CN in SubjectAlternativeName.")
        except x509.ExtensionNotFound:
            raise ValueError("Server CSR must include SubjectAlternativeName.")
    approval = {
        "status": "approved",
        "requester_id": requester_id,
        "cert_type": cert_type,
        "csr_path": str(csr_path),
        "subject": csr.subject.rfc4514_string(),
        "approved_at": now_utc().isoformat(),
        "ra_comment": "CSR signature and identity checked by RA.",
    }
    approval_path = APPROVAL_DIR / f"{requester_id}.approval.json"
    approval_path.write_text(json.dumps(approval, indent=2), encoding="utf-8")
    print(f"RA approved request: {approval_path}")
def ca_sign(approval_path: Path, days: int = 365):
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    if approval["status"] != "approved":
        raise ValueError("CA signs only RA-approved requests.")
    csr = load_csr(Path(approval["csr_path"]))
    ca_key = load_private_key(CA_KEY)
    ca_cert = load_cert(CA_CERT)
    cert_type = approval["cert_type"]
    cn = get_common_name(csr.subject)
    builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now_utc() - dt.timedelta(minutes=5))
        .not_valid_after(now_utc() + dt.timedelta(days=days))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=(cert_type == "server"),
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
        critical=False)
        .add_extension(
            x509.CRLDistributionPoints([
                x509.DistributionPoint(
                    full_name=[x509.UniformResourceIdentifier("file://pki/crl/ca.crl.pem")],
                    relative_name=None,
                    reasons=None,
                    crl_issuer=None,
                )
            ]),
            critical=False,
        )
    )
    if cert_type == "server":
        builder = builder.add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
    else:
        builder = builder.add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]),
            critical=False,
        )
    try:
        san_ext = csr.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        builder = builder.add_extension(san_ext.value, critical=False)
    except x509.ExtensionNotFound:
        pass
    cert = builder.sign(private_key=ca_key, algorithm=hashes.SHA256())
    cert_path = CERT_DIR / f"{cn}.cert.pem"
    save_pem(cert_path, cert.public_bytes(serialization.Encoding.PEM))
    print(f"Certificate issued by CA: {cert_path}")
    print(f"Serial: {cert.serial_number}")
def load_revocations() -> list[dict]:
    if not REVOCATIONS.exists():
        return []
    return json.loads(REVOCATIONS.read_text(encoding="utf-8"))
def save_revocations(items: list[dict]):
    REVOCATIONS.parent.mkdir(parents=True, exist_ok=True)
    REVOCATIONS.write_text(json.dumps(items, indent=2), encoding="utf-8")
def revoke_certificate(cert_path: Path, reason: str = "key_compromise"):
    cert = load_cert(cert_path)
    revocations = load_revocations()
    serial_hex = hex(cert.serial_number)
    if not any(item["serial_hex"] == serial_hex for item in revocations):
        revocations.append({
            "serial": cert.serial_number,
            "serial_hex": serial_hex,
            "revocation_date": now_utc().isoformat(),
            "reason": reason,
            "subject": cert.subject.rfc4514_string(),
        })
        save_revocations(revocations)
    issue_crl()
    print(f"Revoked certificate {cert_path} and updated CRL.")
def issue_crl():
    ensure_dirs()
    ca_key = load_private_key(CA_KEY)
    ca_cert = load_cert(CA_CERT)
    builder = (
        x509.CertificateRevocationListBuilder()
        .issuer_name(ca_cert.subject)
        .last_update(now_utc())
        .next_update(now_utc() + dt.timedelta(days=7))
    )
    reason_map = {
        "key_compromise": x509.ReasonFlags.key_compromise,
        "ca_compromise": x509.ReasonFlags.ca_compromise,
        "affiliation_changed": x509.ReasonFlags.affiliation_changed,
        "superseded": x509.ReasonFlags.superseded,
        "cessation_of_operation": x509.ReasonFlags.cessation_of_operation,
        "certificate_hold": x509.ReasonFlags.certificate_hold,
    }
    for item in load_revocations():
        revoked = (
            x509.RevokedCertificateBuilder()
            .serial_number(int(item["serial"]))
            .revocation_date(dt.datetime.fromisoformat(item["revocation_date"]))
            .add_extension(
                x509.CRLReason(reason_map.get(item["reason"], x509.ReasonFlags.unspecified)),
                critical=False,
            )
            .build()
        )
        builder = builder.add_revoked_certificate(revoked)
    crl = builder.sign(private_key=ca_key, algorithm=hashes.SHA256())
    save_pem(CRL_FILE, crl.public_bytes(serialization.Encoding.PEM))
    print(f"CRL issued: {CRL_FILE}")
def get_not_before(cert):
    if hasattr(cert, "not_valid_before_utc"):
        return cert.not_valid_before_utc
    return cert.not_valid_before.replace(tzinfo=dt.timezone.utc)
def get_not_after(cert):
    if hasattr(cert, "not_valid_after_utc"):
        return cert.not_valid_after_utc
    return cert.not_valid_after.replace(tzinfo=dt.timezone.utc)
def get_crl_next_update(crl):
    if hasattr(crl, "next_update_utc"):
        return crl.next_update_utc
    return crl.next_update.replace(tzinfo=dt.timezone.utc)
def validate_certificate_object(cert: x509.Certificate, purpose: str):
    ca_cert = load_cert(CA_CERT)
    if not CRL_FILE.exists():
        issue_crl()
    crl = load_crl(CRL_FILE)
    # 1) Trust anchor and issuer.
    if cert.issuer != ca_cert.subject:
        raise ValueError("Certificate was not issued by this CA.")
    # 2) Certificate signature.
    rsa_verify_signature(
        ca_cert.public_key(),
        cert.signature,
        cert.tbs_certificate_bytes,
        cert.signature_hash_algorithm,
    )
    # 3) CRL signature and freshness.
    rsa_verify_signature(
        ca_cert.public_key(),
        crl.signature,
        crl.tbs_certlist_bytes,
        crl.signature_hash_algorithm,
    )
    if get_crl_next_update(crl) < now_utc():
        raise ValueError("CRL is expired.")
    # 4) Time validity.
    if not (get_not_before(cert) <= now_utc() <= get_not_after(cert)):
        raise ValueError("Certificate is outside its validity period.")
    # 5) Revocation status.
    for revoked in crl:
        if revoked.serial_number == cert.serial_number:
            raise ValueError(f"Certificate is revoked. serial={hex(cert.serial_number)}")
    # 6) X.509 extensions.
    bc = cert.extensions.get_extension_for_class(x509.BasicConstraints).value
    if bc.ca:
        raise ValueError("End-entity certificate must not be a CA.")
    eku = cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
    if purpose == "server" and ExtendedKeyUsageOID.SERVER_AUTH not in eku:
        raise ValueError("Certificate is not valid for serverAuth.")
    if purpose == "client" and ExtendedKeyUsageOID.CLIENT_AUTH not in eku:
        raise ValueError("Certificate is not valid for clientAuth.")
    return True
def va_verify(cert_path: Path, purpose: str):
    cert = load_cert(cert_path)
    validate_certificate_object(cert, purpose)
    print(f"VA: certificate is valid for {purpose}: {cert_path}")
def run_server(host="127.0.0.1", port=8443):
    import ssl
    # TLS server identity.
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(
        certfile=str(CERT_DIR / "localhost.cert.pem"),
        keyfile=str(KEY_DIR / "localhost.key.pem"),
    )
    # Client authentication with our CA.
    context.load_verify_locations(cafile=str(CA_CERT))
    context.verify_mode = ssl.CERT_REQUIRED
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((host, port))
        sock.listen(5)
        print(f"TLS server listening on {host}:{port}")
        conn, addr = sock.accept()
        with conn:
            with context.wrap_socket(conn, server_side=True) as tls:
                peer_der = tls.getpeercert(binary_form=True)
                peer_cert = x509.load_der_x509_certificate(peer_der)
                validate_certificate_object(peer_cert, "client")
                print("Client certificate passed VA validation.")
                data = tls.recv(4096)
                print("Received:", data.decode("utf-8", errors="replace"))
            tls.sendall(b"secure hello from server")
def run_client(host="127.0.0.1", port=8443):
    import ssl
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile=str(CA_CERT),
    )
    context.load_cert_chain(
        certfile=str(CERT_DIR / "client1.cert.pem"),
        keyfile=str(KEY_DIR / "client1.key.pem"),
    )
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname="localhost") as tls:
            peer_der = tls.getpeercert(binary_form=True)
            peer_cert = x509.load_der_x509_certificate(peer_der)
            validate_certificate_object(peer_cert, "server")
            print("Server certificate passed VA validation.")
            tls.sendall(b"secure hello from client")
            print(tls.recv(4096).decode("utf-8", errors="replace"))
def reset_demo():
    if BASE.exists():
        shutil.rmtree(BASE)
    ensure_dirs()
    create_ca()
    create_csr("localhost", "server")
    ra_approve(REQ_DIR / "localhost.csr.pem", "localhost", "server")
    ca_sign(APPROVAL_DIR / "localhost.approval.json")
    create_csr("client1", "client")
    ra_approve(REQ_DIR / "client1.csr.pem", "client1", "client")
    ca_sign(APPROVAL_DIR / "client1.approval.json")
    issue_crl()
    va_verify(CERT_DIR / "localhost.cert.pem", "server")
    va_verify(CERT_DIR / "client1.cert.pem", "client")
    print("\nDemo PKI is ready. Run server and client in two terminals.")
def main():
    parser = argparse.ArgumentParser(description="Manual PKI lab without openssl CLI.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset-demo")
    sub.add_parser("init-ca")
    p = sub.add_parser("create-csr")
    p.add_argument("--name", required=True, choices=list(VALID_IDENTITIES))
    p.add_argument("--type", required=True, choices=["client", "server"])
    p = sub.add_parser("ra-approve")
    p.add_argument("--csr", required=True)
    p.add_argument("--requester", required=True)
    p.add_argument("--type", required=True, choices=["client", "server"])
    p = sub.add_parser("ca-sign")
    p.add_argument("--approval", required=True)
    p.add_argument("--days", type=int, default=365)
    p = sub.add_parser("verify")
    p.add_argument("--cert", required=True)
    p.add_argument("--purpose", required=True, choices=["client", "server"])
    p = sub.add_parser("revoke")
    p.add_argument("--cert", required=True)
    p.add_argument("--reason", default="key_compromise")
    sub.add_parser("issue-crl")
    sub.add_parser("server")
    sub.add_parser("client")
    args = parser.parse_args()
    if args.cmd == "reset-demo":
        reset_demo()
    elif args.cmd == "init-ca":
        create_ca()
    elif args.cmd == "create-csr":
        create_csr(args.name, args.type)
    elif args.cmd == "ra-approve":
        ra_approve(Path(args.csr), args.requester, args.type)
    elif args.cmd == "ca-sign":
        ca_sign(Path(args.approval), args.days)
    elif args.cmd == "verify":
        va_verify(Path(args.cert), args.purpose)
    elif args.cmd == "revoke":
        revoke_certificate(Path(args.cert), args.reason)
    elif args.cmd == "issue-crl":
        issue_crl()
    elif args.cmd == "server":
        run_server()
    elif args.cmd == "client":
        run_client()
if __name__ == "__main__":
    main()