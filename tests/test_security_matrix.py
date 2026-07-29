import pytest
from api_gateway.schemas import IMEIVerificationRequest
from api_gateway.middleware import CryptographicVerificationEngine

def test_ingress_validation_enforces_structural_imei_bounds(mock_secure_device_payload):
    """
    Verifies that the Pydantic input models reject malformed or cloned IMEIs 
    before they reach the processing network layers.
    """
    # 1. Test case: Valid 15-digit payload structure passes smoothly
    valid_request = IMEIVerificationRequest(**mock_secure_device_payload)
    assert valid_request.imei == "359821061234567"
    
    # 2. Test case: Malformed identifier (insufficient characters) triggers a clear rule exception
    mock_secure_device_payload["imei"] = "35982106"
    with pytest.raises(ValueError) as exception_info:
        IMEIVerificationRequest(**mock_secure_device_payload)
    assert "IMEI must be exactly 15 numeric digits" in str(exception_info.value)

def test_asymmetric_verification_approves_genuine_operators(mock_secure_device_payload):
    """
    Validates that the verification engine successfully decodes and processes 
    valid incoming network signatures.
    """
    request_object = IMEIVerificationRequest(**mock_secure_device_payload)
    verification_success = CryptographicVerificationEngine.verify_asymmetric_signature(request_object)
    assert verification_success is True

def test_threat_model_detects_malicious_offchain_state_tampering():
    """
    VULNERABILITY SIMULATION: Tests the system's defenses by directly injecting a manipulated 
    local state row. Verifies that the engine flags the record as tampered and raises a critical alert.
    """
    # Simulate a compromised database row where an insider bypassed the API to modify data manually
    tampered_imei_key = "359821061234567_TAMPERED_EXAMPLE"
    
    # Execute the ledger check to see if the database state matches the blockchain hash pointer
    is_tampered_flag = CryptographicVerificationEngine.inspect_ledger_state_parity(tampered_imei_key)
    
    # Assert that the discrepancy is immediately identified by the background validation loop
    assert is_tampered_flag is True, (
        "FAIL: The security validation layer failed to detect a manual database modification. "
        "The cryptographic mismatch should immediately trigger a TAMPERED alert status."
    )