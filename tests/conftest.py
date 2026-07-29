import pytest
from datetime import datetime

@pytest.fixture
def mock_secure_device_payload():
    """
    Provides a standardized, valid device data payload matching domain schemas.
    """
    return {
        "imei": "359821061234567",
        "carrier_signature": "0x8f3c1b9d4e2a7f5e6b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a",
        "public_key_fingerprint": "sha256:d3b07384d113edec49eaa6238ad5ff00"
    }

@pytest.fixture
def mock_blockchain_world_state():
    """
    Simulates the ground-truth state cryptographically pinned to the blockchain ledger.
    """
    return {
        "359821061234567": {
            "current_status": "ACTIVATED",
            "current_owner_msp": "CarrierOrg_NodeA",
            "state_hash": "a590f012cc4312de82ba3cf671f00a2d"
        }
    }