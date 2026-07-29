from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class SQLDeviceAsset(Base):
    """
    Represents the off-chain optimized local table structure tracking hardware identities.
    """
    __tablename__ = "telecom_device_inventory"

    imei = Column(String(15), primary_key=True, index=True, nullable=False)
    current_status = Column(String(30), default="REGISTRATION", nullable=False)
    current_owner_msp = Column(String(50), nullable=False)
    public_key_fingerprint = Column(String(64), nullable=False)
    is_compromised = Column(Boolean, default=False, nullable=False)
    last_modified_timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Establishing database relationship vectors
    events = relationship("SQLLifecycleEvent", back_populates="device", cascade="all, delete-orphan")

class SQLLifecycleEvent(Base):
    """
    Tracks local historic data copies mapping directly to the ledger block entries.
    """
    __tablename__ = "telecom_device_audit_trail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_imei = Column(String(15), ForeignKey("telecom_device_inventory.imei", ondelete="CASCADE"), nullable=False)
    transaction_id = Column(String(64), unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    event_type = Column(String(30), nullable=False)
    operator_msp = Column(String(50), nullable=False)

    # Reverse mapping parameter anchors
    device = relationship("SQLDeviceAsset", back_populates="events")