import base64
import json

import pytest
from cryptography.exceptions import InvalidTag
from fastapi.testclient import TestClient

from api_gateway import main as api_main
from event_streaming.consumer import DataLakeIngestionConsumer
from event_streaming.producer import DeviceTelemetryProducer
from offchain_storage.encryption import AES256GCMEncryptionProvider
from offchain_storage.storage_manager import OffChainStorageManager
from provenance_engine.crypto import (
    generate_signing_material,
    sha256_hex,
    sign_payload,
    verify_signature,
)
from provenance_engine.engine import ProvenanceEngine
from provenance_engine.imei import generate_valid_imei, validate_imei


def _build_registry(tmp_path):
    """Create an isolated synthetic registry with genuine and tampered records."""
    genuine_imei = generate_valid_imei()
    tampered_imei = generate_valid_imei()
    while tampered_imei == genuine_imei:
        tampered_imei = generate_valid_imei()

    private_b64, public_b64 = generate_signing_material()

    genuine_genesis = {
        "imei": genuine_imei,
        "manufacturer": "SYNTHETIC_OEM",
        "created_at": "2026-08-19T00:00:00+00:00",
    }
    genuine_current = {
        "imei": genuine_imei,
        "status": "ACTIVATED",
        "owner": "SYNTHETIC_CARRIER",
        "manufacturer": "SYNTHETIC_OEM",
    }

    tampered_genesis = {
        "imei": tampered_imei,
        "manufacturer": "SYNTHETIC_OEM",
        "created_at": "2026-08-19T00:00:00+00:00",
    }
    original_tampered_current = {
        "imei": tampered_imei,
        "status": "ACTIVATED",
        "owner": "SYNTHETIC_CARRIER",
        "manufacturer": "SYNTHETIC_OEM",
    }
    modified_tampered_current = dict(original_tampered_current)
    modified_tampered_current["owner"] = "UNAUTHORIZED_TEST_MUTATION"

    lifecycle = [
        {
            "block_index": 1,
            "timestamp": "2026-08-19T00:00:00+00:00",
            "event_type": "REGISTRATION",
            "authorized_operator": "SYNTHETIC_OEM",
        }
    ]

    registry = {
        "schema_version": 1,
        "purpose": "Generated synthetic test registry; not real device data.",
        "devices": [
            {
                "imei": genuine_imei,
                "fixture_type": "SYNTHETIC_GENUINE",
                "genesis_payload": genuine_genesis,
                "manufacturer_public_key": public_b64,
                "manufacturer_signature": sign_payload(private_b64, genuine_genesis),
                "anchored_hash": sha256_hex(genuine_current),
                "current_record": genuine_current,
                "lifecycle_history": lifecycle,
            },
            {
                "imei": tampered_imei,
                "fixture_type": "SYNTHETIC_TAMPERED",
                "genesis_payload": tampered_genesis,
                "manufacturer_public_key": public_b64,
                "manufacturer_signature": sign_payload(private_b64, tampered_genesis),
                # Anchor the legitimate state, then persist a changed state.
                "anchored_hash": sha256_hex(original_tampered_current),
                "current_record": modified_tampered_current,
                "lifecycle_history": lifecycle,
            },
        ],
    }

    registry_path = tmp_path / "device_registry.json"
    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return registry_path, genuine_imei, tampered_imei


def test_generated_imei_passes_structural_and_luhn_validation():
    """Generated synthetic IMEIs must satisfy the prototype's 15-digit check."""
    imei = generate_valid_imei()
    valid, reason = validate_imei(imei)

    assert len(imei) == 15
    assert imei.isdigit()
    assert valid is True
    assert reason == "VALID"


def test_shared_engine_exposes_all_four_authenticity_states(tmp_path):
    """The shared engine must distinguish GENUINE, TAMPERED, UNKNOWN and INVALID."""
    registry_path, genuine_imei, tampered_imei = _build_registry(tmp_path)
    engine = ProvenanceEngine(registry_path)

    unknown_imei = generate_valid_imei()
    while unknown_imei in {genuine_imei, tampered_imei}:
        unknown_imei = generate_valid_imei()

    genuine = engine.verify(genuine_imei)
    tampered = engine.verify(tampered_imei)
    unknown = engine.verify(unknown_imei)
    invalid = engine.verify("35982106")

    assert genuine.authenticity_state == "GENUINE"
    assert genuine.is_genuine is True
    assert genuine.is_tampered is False
    assert genuine.signature_valid is True
    assert genuine.hash_integrity_valid is True

    assert tampered.authenticity_state == "TAMPERED"
    assert tampered.is_genuine is False
    assert tampered.is_tampered is True
    assert tampered.signature_valid is True
    assert tampered.hash_integrity_valid is False

    assert unknown.authenticity_state == "UNKNOWN"
    assert unknown.current_status == "NOT_REGISTERED"
    assert unknown.signature_valid is None
    assert unknown.hash_integrity_valid is None

    assert invalid.authenticity_state == "INVALID"
    assert invalid.current_status == "INVALID_INPUT"
    assert invalid.signature_valid is None
    assert invalid.hash_integrity_valid is None


def test_real_ecdsa_p256_signature_rejects_modified_payload():
    """A valid ECDSA P-256 signature must fail after payload modification."""
    private_b64, public_b64 = generate_signing_material()
    payload = {"imei": generate_valid_imei(), "manufacturer": "SYNTHETIC_OEM"}
    signature_b64 = sign_payload(private_b64, payload)

    assert verify_signature(public_b64, payload, signature_b64) is True

    modified_payload = dict(payload)
    modified_payload["manufacturer"] = "UNAUTHORIZED_MUTATION"
    assert verify_signature(public_b64, modified_payload, signature_b64) is False


def test_aes256_gcm_detects_ciphertext_tampering():
    """Authenticated encryption must reject a modified ciphertext."""
    provider = AES256GCMEncryptionProvider()
    associated_data = b"synthetic-device-manifest"
    encrypted = provider.encrypt(b"prototype evidence payload", associated_data)

    ciphertext = bytearray(base64.b64decode(encrypted["ciphertext"]))
    ciphertext[0] ^= 0x01
    tampered_b64 = base64.b64encode(bytes(ciphertext)).decode("ascii")

    with pytest.raises(InvalidTag):
        provider.decrypt(encrypted["nonce"], tampered_b64, associated_data)


def test_encrypted_offchain_storage_round_trip(tmp_path):
    """Archived plaintext must be recoverable through the encrypted prototype vault."""
    manager = OffChainStorageManager(
        key=AES256GCMEncryptionProvider().key,
        archive_dir=tmp_path / "vault",
    )
    raw_content = json.dumps(
        {"imei": generate_valid_imei(), "purpose": "SYNTHETIC_TEST_ONLY"},
        sort_keys=True,
    )

    receipt = manager.archive_device_manifest("synthetic_manifest.json", raw_content)
    restored = manager.restore_device_manifest(receipt["offchain_uri"])

    assert receipt["algorithm"] == "AES-256-GCM"
    assert receipt["storage_provider"] == "LOCAL_ENCRYPTED_PROTOTYPE_VAULT"
    assert restored == raw_content


def test_api_and_shared_engine_return_consistent_genuine_result(tmp_path, monkeypatch):
    """The FastAPI endpoint must delegate classification to the shared provenance engine."""
    registry_path, genuine_imei, _ = _build_registry(tmp_path)
    isolated_engine = ProvenanceEngine(registry_path)
    monkeypatch.setattr(api_main, "engine", isolated_engine)

    expected = isolated_engine.verify(genuine_imei).to_dict()
    response = TestClient(api_main.app).post(
        "/api/v1/provenance/verify",
        json={"imei": genuine_imei, "requesting_msp": "CarrierMSP"},
    )

    assert response.status_code == 200
    actual = response.json()
    assert actual["authenticity_state"] == expected["authenticity_state"] == "GENUINE"
    assert actual["signature_valid"] == expected["signature_valid"] is True
    assert actual["hash_integrity_valid"] == expected["hash_integrity_valid"] is True


def test_streaming_path_is_explicitly_labeled_as_simulation():
    """Producer/consumer behavior must not imply that a live Kafka broker was contacted."""
    producer = DeviceTelemetryProducer()
    consumer = DataLakeIngestionConsumer()
    imei = generate_valid_imei()

    emitted = producer.emit_lifecycle_event(imei, "ACTIVATION", "SYNTHETIC_CARRIER")
    processed = consumer.process_incoming_stream_packet(emitted["packet"])

    assert emitted["status"] == "SIMULATED_EMIT"
    assert processed["status"] == "SIMULATED_PROCESS"
    assert processed["payload"]["simulation"] is True
    assert processed["payload"]["imei"] == imei


def test_api_returns_invalid_state_for_malformed_imei(monkeypatch, tmp_path):
    """Malformed input is represented by the prototype's explicit INVALID state."""
    registry_path, _, _ = _build_registry(tmp_path)
    monkeypatch.setattr(api_main, "engine", ProvenanceEngine(registry_path))

    response = TestClient(api_main.app).post(
        "/api/v1/provenance/verify",
        json={"imei": "35982106", "requesting_msp": "CarrierMSP"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["authenticity_state"] == "INVALID"
    assert body["current_status"] == "INVALID_INPUT"
    assert body["is_genuine"] is False
    assert body["is_tampered"] is False


def test_unknown_means_valid_but_not_registered(tmp_path):
    """UNKNOWN must be semantically distinct from INVALID and TAMPERED."""
    registry_path, genuine_imei, tampered_imei = _build_registry(tmp_path)
    engine = ProvenanceEngine(registry_path)

    unknown_imei = generate_valid_imei()
    while unknown_imei in {genuine_imei, tampered_imei}:
        unknown_imei = generate_valid_imei()

    valid, _ = validate_imei(unknown_imei)
    result = engine.verify(unknown_imei)

    assert valid is True
    assert result.authenticity_state == "UNKNOWN"
    assert result.current_status == "NOT_REGISTERED"
    assert result.is_genuine is False
    assert result.is_tampered is False
    assert "no matching record" in result.reason.lower()