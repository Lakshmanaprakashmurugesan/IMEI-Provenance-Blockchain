from dataclasses import dataclass, asdict
from pathlib import Path
import json
from .imei import validate_imei
from .crypto import sha256_hex, verify_signature
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = ROOT / "data" / "device_registry.json"

@dataclass
class VerificationResult:
    imei: str; authenticity_state: str; is_genuine: bool; is_tampered: bool
    current_status: str; current_owner: str; signature_valid: bool|None
    hash_integrity_valid: bool|None; reason: str; lifecycle_history: list
    data_source: str = "Shared Provenance Engine"
    def to_dict(self): return asdict(self)

class ProvenanceEngine:
    def __init__(self, registry_path=DEFAULT_REGISTRY): self.registry_path = Path(registry_path)
    def _load(self):
        if not self.registry_path.exists(): return {"devices": []}
        data = json.loads(self.registry_path.read_text(encoding="utf-8"))
        if not isinstance(data.get("devices", []), list): raise ValueError("Invalid registry structure")
        return data
    def find_device(self, imei):
        return next((x for x in self._load()["devices"] if x.get("imei") == imei), None)
    def verify(self, imei):
        valid, reason = validate_imei(imei)
        if not valid:
            return VerificationResult(imei,"INVALID",False,False,"INVALID_INPUT","NOT_AVAILABLE",None,None,reason,[])
        record = self.find_device(imei)
        if record is None:
            return VerificationResult(imei,"UNKNOWN",False,False,"NOT_REGISTERED","NOT_AVAILABLE",None,None,
                                      "Valid IMEI, but no matching record exists in the prototype registry.",[])
        sig_ok = verify_signature(record.get("manufacturer_public_key",""), record.get("genesis_payload",{}), record.get("manufacturer_signature",""))
        current = record.get("current_record",{})
        hash_ok = sha256_hex(current) == record.get("anchored_hash")
        tampered = not sig_ok or not hash_ok
        why=[]
        if not sig_ok: why.append("manufacturer signature verification failed")
        if not hash_ok: why.append("current record hash does not match anchored hash")
        if not why: why.append("manufacturer signature and anchored record hash both verify")
        return VerificationResult(imei,"TAMPERED" if tampered else "GENUINE",not tampered,tampered,
            "TAMPER_LOCKDOWN" if tampered else current.get("status","UNKNOWN"),
            "SYSTEM_ALERT" if tampered else current.get("owner","NOT_AVAILABLE"),sig_ok,hash_ok,"; ".join(why)+".",record.get("lifecycle_history",[]))
