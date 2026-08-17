import base64, hashlib, json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def canonical_bytes(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(payload):
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def generate_signing_material():
    """Generate an ECDSA P-256 keypair encoded as base64 DER."""
    private = ec.generate_private_key(ec.SECP256R1())
    public = private.public_key()
    private_der = private.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_der = public.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return base64.b64encode(private_der).decode("ascii"), base64.b64encode(public_der).decode("ascii")


def sign_payload(private_b64, payload):
    private = serialization.load_der_private_key(base64.b64decode(private_b64), password=None)
    if not isinstance(private, ec.EllipticCurvePrivateKey):
        raise TypeError("Expected EC private key")
    signature = private.sign(canonical_bytes(payload), ec.ECDSA(hashes.SHA256()))
    return base64.b64encode(signature).decode("ascii")


def verify_signature(public_b64, payload, signature_b64):
    try:
        public = serialization.load_der_public_key(base64.b64decode(public_b64))
        if not isinstance(public, ec.EllipticCurvePublicKey):
            return False
        public.verify(
            base64.b64decode(signature_b64),
            canonical_bytes(payload),
            ec.ECDSA(hashes.SHA256()),
        )
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False
