from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class DeviceStatusEnum(str, Enum):
    REGISTRATION = "REGISTRATION"
    CUSTODY_TRANSFER = "CUSTODY_TRANSFER"
    ACTIVATED = "ACTIVATED"
    BLACKLIST = "BLACKLIST"
    DECOMMISSIONED = "DECOMMISSIONED"

class DomainLifecycleEventContract(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction hash link from the ledger block")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: DeviceStatusEnum = Field(..., description="Valid categorical state tracking key")
    operator_msp: str = Field(..., description="The membership service provider ID executing the change")

    class Config:
        from_attributes = True

class DomainDeviceContract(BaseModel):
    imei: str = Field(..., description="Unique 15-digit hardware signature token")
    current_status: DeviceStatusEnum = Field(..., default=DeviceStatusEnum.REGISTRATION)
    current_owner_msp: str = Field(..., description="The entity managing active inventory custody")
    public_key_fingerprint: str = Field(..., description="The asymmetric signing root anchor hash")
    is_compromised: bool = Field(default=False)
    last_modified_timestamp: datetime = Field(default_factory=datetime.utcnow)
    history_trail: List[DomainLifecycleEventContract] = Field(default=[])

    @field_validator('imei')
    @classmethod
    def enforce_strict_imei_bounds(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 15:
            raise ValueError("Data contract validation error: IMEI must be exactly 15 numeric digits.")
        return value

    class Config:
        from_attributes = True