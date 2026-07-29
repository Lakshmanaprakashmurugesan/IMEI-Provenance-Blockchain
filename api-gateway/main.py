from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from datetime import datetime
from api_gateway.config import settings
from api_gateway.schemas import IMEIVerificationRequest, VerificationResponse, LifecycleEvent
from api_gateway.middleware import CryptographicVerificationEngine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs"
)

# Mocked state dictionary to simulate real-time blockchain ledger entries
MOCK_LEDGER_STATE = {
    "359821061234567": {
        "current_status": "ACTIVATED",
        "current_owner": "Carrier_Node_A",
        "history": [
            {"block_index": 1, "event_type": "REGISTRATION", "operator": "OEM_ORIGIN"},
            {"block_index": 2, "event_type": "CUSTODY_TRANSFER", "operator": "Carrier_Node_A"}
        ]
    }
}

@app.post(
    f"{settings.API_V1_STR}/provenance/verify", 
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest and Verify Device Assets"
)
async def verify_device_provenance(payload: IMEIVerificationRequest):
    # 1. Run the asymmetric signature check
    is_signature_valid = CryptographicVerificationEngine.verify_asymmetric_signature(payload)
    if not is_signature_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cryptographic signing token validation failed. Unauthorized asset genesis rejected."
        )

    # 2. Check for off-chain state tampering
    is_tampered_state = CryptographicVerificationEngine.inspect_ledger_state_parity(payload.imei)
    
    # 3. Pull ledger records
    device_record = MOCK_LEDGER_STATE.get(
        payload.imei, 
        {"current_status": "UNKNOWN", "current_owner": "UNREGISTERED", "history": []}
    )
    
    # Map raw data lists into structured Pydantic object layers
    formatted_history = [
        LifecycleEvent(
            block_index=item["block_index"],
            timestamp=datetime.utcnow(),
            event_type=item["event_type"],
            authorized_operator=item["operator"]
        ) for item in device_record["history"]
    ]

    return VerificationResponse(
        imei=payload.imei,
        is_genuine=not is_tampered_state and payload.imei in MOCK_LEDGER_STATE,
        current_status="TAMPER_LOCKDOWN" if is_tampered_state else device_record["current_status"],
        current_owner="SYSTEM_ALERT" if is_tampered_state else device_record["current_owner"],
        is_tampered=is_tampered_state,
        lifecycle_history=formatted_history
    )