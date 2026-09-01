"""Security helpers used by the API.

Unlike the earlier length-based signature placeholder, cryptographic authenticity
is now evaluated by the shared provenance engine using ECDSA P-256 verification and
SHA-256 record integrity checks.
"""
from provenance_engine.engine import ProvenanceEngine

class CryptographicVerificationEngine:
    @staticmethod
    def verify_device(imei: str):
        return ProvenanceEngine().verify(imei)

    @staticmethod
    def inspect_ledger_state_parity(imei: str) -> bool:
        return ProvenanceEngine().verify(imei).is_tampered
