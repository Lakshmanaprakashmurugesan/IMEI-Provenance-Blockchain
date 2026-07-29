import os

class OffChainStorageConfig:
    # Storage Volume Directives
    LOCAL_MOUNT_DIR: str = "/data/offchain_vault"
    ENCRYPTED_ARCHIVE_DIR: str = "/data/offchain_vault/encrypted"
    
    # Cryptographic Constraints
    HASH_ALGORITHM: str = "sha256"
    CIPHER_ALGORITHM: str = "AES-256-GCM"
    
    # Performance Parameters
    CHUNK_SIZE_BYTES: int = 65536  # 64KB file read buffer block allocation

storage_config = OffChainStorageConfig()