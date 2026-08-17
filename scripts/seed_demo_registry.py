import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from provenance_engine.crypto import generate_signing_material, sign_payload, sha256_hex
from provenance_engine.imei import generate_valid_imei
REG=ROOT/'data'/'device_registry.json'; OUT=ROOT/'evidence'/'demo_test_values.json'
def build(imei,tampered):
    private,public=generate_signing_material(); now=datetime.now(timezone.utc).isoformat()
    genesis={"imei":imei,"manufacturer":"SYNTHETIC_OEM","created_at":now}; sig=sign_payload(private,genesis)
    current={"imei":imei,"status":"ACTIVATED","owner":"SYNTHETIC_CARRIER","manufacturer":"SYNTHETIC_OEM"}; anchor=sha256_hex(current)
    history=[{"block_index":1,"timestamp":now,"event_type":"REGISTRATION","authorized_operator":"SYNTHETIC_OEM"},{"block_index":2,"timestamp":now,"event_type":"CUSTODY_TRANSFER","authorized_operator":"SYNTHETIC_CARRIER"},{"block_index":3,"timestamp":now,"event_type":"ACTIVATION","authorized_operator":"SYNTHETIC_CARRIER"}]
    if tampered: current["owner"]="UNAUTHORIZED_TEST_MUTATION"
    return {"imei":imei,"fixture_type":"SYNTHETIC_TAMPERED" if tampered else "SYNTHETIC_GENUINE","genesis_payload":genesis,"manufacturer_public_key":public,"manufacturer_signature":sig,"anchored_hash":anchor,"current_record":current,"lifecycle_history":history}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--reset',action='store_true'); a=p.parse_args()
    if REG.exists() and not a.reset: print('Registry already exists; use --reset to regenerate.'); return
    g=generate_valid_imei(); t=generate_valid_imei()
    while t==g: t=generate_valid_imei()
    u=generate_valid_imei()
    while u in {g,t}: u=generate_valid_imei()
    REG.parent.mkdir(parents=True,exist_ok=True); OUT.parent.mkdir(parents=True,exist_ok=True)
    REG.write_text(json.dumps({"schema_version":1,"purpose":"Generated synthetic test registry; not real device data.","devices":[build(g,False),build(t,True)]},indent=2),encoding='utf-8')
    OUT.write_text(json.dumps({"generated_at":datetime.now(timezone.utc).isoformat(),"genuine_imei":g,"tampered_imei":t,"unknown_imei":u,"invalid_imei":"123"},indent=2),encoding='utf-8')
    print(f'GENUINE test IMEI : {g}'); print(f'TAMPERED test IMEI: {t}'); print(f'UNKNOWN test IMEI : {u}'); print('INVALID test IMEI : 123')
if __name__=='__main__': main()
