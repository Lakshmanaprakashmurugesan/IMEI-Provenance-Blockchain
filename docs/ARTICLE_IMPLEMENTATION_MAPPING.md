# Article-to-Repository Implementation Mapping

This repository is a **technical prototype/reference implementation** of selected mechanisms described in the published IMEI provenance architecture. It does not claim to reproduce production-scale deployment figures.

| Published architecture capability | Repository implementation | Current validation / status |
|---|---|---|
| IMEI identity validation | `provenance_engine/imei.py` | 15 digits + IMEI/Luhn check digit; Pytest |
| Shared provenance decision logic | `provenance_engine/engine.py` | API and dashboard fallback use the same engine |
| OEM genesis signature | `provenance_engine/crypto.py` + generated registry records | Real Ed25519 sign/verify test |
| Hash-based tamper detection | `provenance_engine/engine.py` | SHA-256 comparison against anchored hash; tamper fixture test |
| GENUINE / TAMPERED / UNKNOWN / INVALID | shared provenance engine | Automated four-state test |
| API gateway | `api_gateway/` | FastAPI TestClient validation |
| Lifecycle smart-contract logic | `chaincode/imei/` | Go transition rules + Go test source |
| Permissioned Fabric configuration | `network-config/` | Configuration/reference only; no running Fabric network in this ZIP |
| Encrypted off-chain records | `offchain_storage/` | Real AES-256-GCM + actual encrypted file persistence + restore test |
| Hash reference for off-chain content | `offchain_storage/storage_manager.py` | SHA-256 plaintext reference returned with archive metadata |
| Event streaming | `event_streaming/` | Explicitly labeled Kafka-compatible simulation; no broker claim |
| Event evidence | `evidence/event_stream_log.csv` | Runtime-generated; simulation status labels are explicit |
| Security evidence | `evidence/security_event_log.csv` | Runtime-generated from detected conditions |
| Control tower | `dashboard/app.py` | Streamlit UI; syntax checked in validation environment |
| Automated validation | `tests/`, `run_validation.py` | Pytest XML + console evidence |
| Docker | `docker/`, `docker-compose.yml` | API + dashboard containers only; no Kafka/Fabric deployment claim |

## Important boundary

The repository demonstrates inspectable implementation progress and prototype mechanisms. It should not be described as evidence of national carrier deployment, production throughput, production fraud-reduction metrics, 68 peers, 190M API calls, EKS/Kubernetes operation, or other production-scale claims unless separate contemporaneous evidence exists.
