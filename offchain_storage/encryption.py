import os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AES256GCMEncryptionProvider:
    """Real AES-256-GCM authenticated encryption with a fresh 96-bit nonce."""
    def __init__(self, key: bytes | None = None):
        key = key or AESGCM.generate_key(bit_length=256)
        if len(key) != 32: raise ValueError("AES-256-GCM requires a 32-byte key")
        self.key=key; self.aesgcm=AESGCM(key)
    def encrypt(self, raw_data: bytes, associated_data: bytes | None=None) -> dict:
        nonce=os.urandom(12); ciphertext=self.aesgcm.encrypt(nonce,raw_data,associated_data)
        return {"algorithm":"AES-256-GCM","nonce":base64.b64encode(nonce).decode(),"ciphertext":base64.b64encode(ciphertext).decode()}
    def decrypt(self, nonce_b64: str, ciphertext_b64: str, associated_data: bytes | None=None) -> bytes:
        return self.aesgcm.decrypt(base64.b64decode(nonce_b64),base64.b64decode(ciphertext_b64),associated_data)
    def export_key_base64(self): return base64.b64encode(self.key).decode()
    @staticmethod
    def load_key_base64(value):
        key=base64.b64decode(value)
        if len(key)!=32: raise ValueError("Decoded AES key must be exactly 32 bytes")
        return key
