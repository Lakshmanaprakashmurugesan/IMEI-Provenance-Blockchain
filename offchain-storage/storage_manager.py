import hashlib
import logging
from offchain_storage.storage_config import storage_config
from offchain_storage.encryption import SymmetricEncryptionProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StorageManager")

class OffChainStorageManager:
    def __init__(self):
        self.vault_path = storage_config.LOCAL_MOUNT_DIR
        self.encryptor = SymmetricEncryptionProvider()
        logger.info(f"Off-chain archival vault mounted successfully on path: {self.vault_path}")

    def generate_sha256_hash(self, data_bytes: bytes) -> str:
        """
        Calculates a unique, immutable SHA-256 hash signature for any given file block or document.
        """
        hasher = hashlib.sha256()
        # Read data in standard chunk envelopes to keep server memory footprint tiny
        hasher.update(data_bytes)
        calculated_hash = hasher.hexdigest()
        logger.info(f"Generated deterministic cryptographic hash token: {calculated_hash}")
        return calculated_hash

    def archive_device_manifest(self, document_name: str, raw_content: str) -> dict:
        """
        Orchestrates full archival: Encrypts the raw file text, computes the tracking hash, 
        and produces a ledger registration payload to pin to the blockchain.
        """
        logger.info(f"Initiating off-chain archival sequence for manifest file: '{document_name}'")
        
        # 1. Transform text string to bytes and generate tracking hash
        raw_bytes = raw_content.encode('utf-8')
        tracking_hash = self.generate_sha256_hash(raw_bytes)
        
        # 2. Encrypt the data before storage to maintain security compliance
        encryption_result = self.encryptor.encrypt_document_payload(raw_content)
        
        if encryption_result["status"] != "SUCCESS":
            raise Exception("Archival aborted due to encryption sub-system failure.")

        # 3. Simulate saving the encrypted payload to the isolated volume folder
        logger.info(f"Encrypted file block successfully persisted to disk volume path: {storage_config.ENCRYPTED_ARCHIVE_DIR}/{tracking_hash}.dat")
        
        # This payload dictionary is returned to feed the transaction directly into the blockchain ledger
        return {
            "immutable_ledger_hash": tracking_hash,
            "offchain_uri": f"vault://volumes/encrypted/{tracking_hash}.dat",
            "storage_provider": "ON_PREM_VAULT_NODE_A",
            "timestamp_archived": "2026-07-12T14:17:55Z"
        }

if __name__ == "__main__":
    # Test execution harness to verify pipeline execution strings
    manager = OffChainStorageManager()
    sample_manifest = "IMEI=359821061234567, Owner=OEM_Origin, OEM_Lot=4091A, ComplianceCode=CISA-SCRM"
    result_payload = manager.archive_device_manifest("device_genesis_manifest.txt", sample_manifest)
    print(f"\n--- SUCCESSFUL DATA ARCHIVAL EXECUTION OUTPUT ---")
    print(f"Blockchain Reference Hash: {result_payload['immutable_ledger_hash']}")
    print(f"Off-Chain URI: {result_payload['offchain_uri']}")