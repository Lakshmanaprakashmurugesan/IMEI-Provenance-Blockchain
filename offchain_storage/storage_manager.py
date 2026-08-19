import hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
from .storage_config import storage_config
from .encryption import AES256GCMEncryptionProvider

class OffChainStorageManager:
    def __init__(self, key: bytes | None=None, archive_dir: Path | None=None):
        self.archive_dir=Path(archive_dir or storage_config.ENCRYPTED_ARCHIVE_DIR); self.archive_dir.mkdir(parents=True,exist_ok=True)
        self.encryptor=AES256GCMEncryptionProvider(key or self._load_or_create_local_key())
    def _load_or_create_local_key(self):
        env=os.getenv("IMEI_AES_KEY_B64")
        if env: return AES256GCMEncryptionProvider.load_key_base64(env)
        path=storage_config.KEY_FILE; path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists(): return AES256GCMEncryptionProvider.load_key_base64(path.read_text().strip())
        provider=AES256GCMEncryptionProvider(); path.write_text(provider.export_key_base64(),encoding="utf-8")
        return provider.key
    @staticmethod
    def generate_sha256_hash(data_bytes: bytes) -> str: return hashlib.sha256(data_bytes).hexdigest()
    def archive_device_manifest(self, document_name: str, raw_content: str) -> dict:
        raw=raw_content.encode(); digest=self.generate_sha256_hash(raw); aad=document_name.encode()
        encrypted=self.encryptor.encrypt(raw,aad)
        envelope={"document_name":document_name,"plaintext_sha256":digest,"algorithm":encrypted["algorithm"],"nonce":encrypted["nonce"],"ciphertext":encrypted["ciphertext"]}
        target=self.archive_dir/f"{digest}.json"; target.write_text(json.dumps(envelope,indent=2),encoding="utf-8")
        root=Path(__file__).resolve().parent.parent
        try:
            uri=str(target.relative_to(root)).replace('\\','/')
        except ValueError:
            uri=str(target.resolve())
        return {"immutable_ledger_hash":digest,"offchain_uri":uri,"storage_provider":"LOCAL_ENCRYPTED_PROTOTYPE_VAULT","timestamp_archived":datetime.now(timezone.utc).isoformat(),"algorithm":"AES-256-GCM"}
    def restore_device_manifest(self, relative_uri: str) -> str:
        root=Path(__file__).resolve().parent.parent; candidate=Path(relative_uri); target=candidate if candidate.is_absolute() else root/candidate; envelope=json.loads(target.read_text(encoding="utf-8"))
        clear=self.encryptor.decrypt(envelope["nonce"],envelope["ciphertext"],envelope["document_name"].encode())
        if self.generate_sha256_hash(clear)!=envelope["plaintext_sha256"]: raise ValueError("Restored manifest hash mismatch")
        return clear.decode()
