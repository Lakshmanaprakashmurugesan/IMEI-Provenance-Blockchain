from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from provenance_engine.imei import validate_imei

class LifecycleEvent(BaseModel):
    block_index: int
    timestamp: datetime | str
    event_type: str
    authorized_operator: str

class IMEIVerificationRequest(BaseModel):
    imei: str = Field(..., description="15-digit IMEI with valid check digit")
    requesting_msp: str = Field(default="CarrierMSP")



class VerificationResponse(BaseModel):
    imei: str
    authenticity_state: str
    is_genuine: bool
    current_status: str
    current_owner: str
    is_tampered: bool
    signature_valid: bool | None = None
    hash_integrity_valid: bool | None = None
    reason: str
    lifecycle_history: List[LifecycleEvent]
