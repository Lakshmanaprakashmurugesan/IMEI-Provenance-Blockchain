from fastapi import FastAPI
from api_gateway.config import settings
from api_gateway.schemas import IMEIVerificationRequest, VerificationResponse
from provenance_engine.engine import ProvenanceEngine

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, docs_url="/docs")
engine = ProvenanceEngine()

@app.get("/health")
def health():
    return {"status":"ok","mode":"prototype","provenance_engine":"shared-local-registry"}

@app.post(f"{settings.API_V1_STR}/provenance/verify", response_model=VerificationResponse)
def verify_device_provenance(payload: IMEIVerificationRequest):
    return engine.verify(payload.imei).to_dict()
