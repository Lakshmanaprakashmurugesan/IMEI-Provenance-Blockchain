from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class LifecycleEvent(BaseModel):
    block_index: int = Field(..., description="Sequential block pointer on the permissioned ledger")
    timestamp: datetime = Field(..., default_factory=datetime.utcnow)
    event_type: str = Field(..., description="Operational event state: REGISTRATION, TRANSFER, ACTIVATION, BLACKLIST")
    authorized_operator: str = Field(..., description="The unique MSP Identifier of the initiating carrier node")

class IMEIVerificationRequest(BaseModel):
    imei: str = Field(..., description="The unique 15-digit International Mobile Equipment Identity string")
    carrier_signature: str = Field(..., description="Hexadecimal asymmetric digital signature validating identity genesis")
    public_key_fingerprint: str = Field(..., description="The SHA-256 fingerprint tracking the signing certificate path")

    @field_validator('imei')
    @classmethod
    def validate_imei_format(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 15:
            raise ValueError("Invalid asset identifier format. IMEI must be exactly 15 numeric digits.")
        return value

class VerificationResponse(BaseModel):
    imei: str
    is_genuine: bool
    current_status: str
    current_owner: str
    is_tampered: bool
    lifecycle_history: List[LifecycleEvent]