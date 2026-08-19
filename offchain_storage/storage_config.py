import os
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
class OffChainStorageConfig:
    ENCRYPTED_ARCHIVE_DIR: Path = Path(os.getenv("IMEI_ENCRYPTED_ARCHIVE_DIR", str(ROOT/"evidence"/"offchain_vault"/"encrypted")))
    KEY_FILE: Path = Path(os.getenv("IMEI_LOCAL_AES_KEY_FILE", str(ROOT/".local_keys"/"offchain_aes256.key")))
    HASH_ALGORITHM="sha256"; CIPHER_ALGORITHM="AES-256-GCM"
storage_config=OffChainStorageConfig()
