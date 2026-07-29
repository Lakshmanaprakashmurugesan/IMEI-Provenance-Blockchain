# Enterprise Blockchain-Based IMEI Provenance System

A production-grade, permissioned blockchain architecture designed to establish immutable device provenance, eliminate counterfeit telecommunications equipment infiltration, and secure cross-carrier device tracking infrastructure[cite: 1].

This repository implements **Pillar 1 (The Cryptographic Trust Layer)** of a distributed telecommunications supply-chain resilience framework[cite: 1]. It functions as a secure identity anchor, providing clean, tamper-evident hardware asset lifecycle records to downstream analytics pipelines and Multi-Echelon Inventory Optimization (MEIO) models[cite: 1].

---

## 📰 Peer-Reviewed Publication & Reference

The theoretical framework, threat model, and performance metrics animating this architecture have been peer-reviewed and formally published in the *Silicon Valleys Journal*[cite: 1]. 

- **Article Title:** Securing the Link: A Blockchain-Based IMEI Provenance System for Telecom Security[cite: 1]
- **Author:** Lakshmanaprakash Murugesan[cite: 1]
- **Publication Date:** December 1, 2025[cite: 1]
- **Verified Publication Link:** https://siliconvalleysjournal.com/2025/12/01/securing-the-link-a-blockchain-based-imei-provenance-system-for-telecom-security/[cite: 1]

---

## 🏗️ Technical Architecture & Ledger Protocols

The platform architecture is divided into decoupled microservices running across a permissioned ledger network[cite: 1]:

1. **Cryptographic Provenance Layer (/chaincode)**: Implements Go-based smart contracts running on an orchestrated Hyperledger Fabric v2.5 framework[cite: 1]. It enforces deterministic state changes across the entire asset lifecycle: from OEM manufacturing genesis, through distributor transfers and warehouse custody, to retail activation, blacklisting, and decommissioning[cite: 1].
2. **Asymmetric Verification Middleware (/api-gateway)**: Enforces secure ingestion using digital signatures before transactions ever commit to the ledger, completely mitigating IMEI cloning, identity spoofing, and unauthorized data injection[cite: 1].
3. **Off-Chain Encrypted Storage (/offchain-storage)**: Preserves carrier and regulatory data privacy standards by excluding all personally identifiable information (PII) from the shared state[cite: 1]. Large operational compliance records and repair logs are held in encrypted off-chain repositories; only their unique cryptographic SHA-256 hashes are appended to the blockchain ledger to maintain national-scale transaction finality[cite: 1].
4. **Event-Streaming Pipeline (/event-streaming)**: A Kafka-compatible distributed messaging topology architected to normalize and ingest between 5 and 8 terabytes of transactional lifecycle data per month into a shared cloud data lake[cite: 1].

---

## 📁 Repository Directory Structure

The workspace is organized into the following clean, modular layout[cite: 1]:

imei-provenance-blockchain/
├── api-gateway/       # FastAPI REST Controllers, security middleware, and configurations[cite: 1]
├── chaincode/         # Go-based Hyperledger Fabric smart contracts and world state schemas[cite: 1]
├── network-config/    # Multi-MSP governance profiles, Raft specs, and CA connections[cite: 1]
├── event-streaming/   # Kafka pub/sub messaging channel producers, consumers, and sinks[cite: 1]
├── offchain-storage/  # Document encryption handlers and SHA-256 hash routines[cite: 1]
├── dashboard/         # Control Tower Streamlit UI displaying real-time tracking telemetry[cite: 1]
├── models/            # Privacy-preserving Pydantic request models and SQL mappings[cite: 1]
├── tests/             # Automated unit checks and security threat exploit simulation suites[cite: 1]
└── docker/            # Container environment files and Kubernetes (EKS) templates[cite: 1]

---

## 🖥️ System Outputs & Generated Deliverables

When the infrastructure is fully compiled and deployed via Docker, the system exposes three primary runtime outputs[cite: 1]:

### 1. The Interactive API Gateway Manager (FastAPI Swagger UI)
- **Interface Access:** Accessible locally at http://localhost:8000/docs[cite: 1]
- **Output Artifact:** A live web terminal hosting structured RESTful endpoints[cite: 1]. When executing an IMEI validation request, it outputs a strict, privacy-preserving cryptographic JSON data block tracking device custody history without exposing private customer information[cite: 1]:

{
  "imei": "359821061234567",
  "is_genuine": true,
  "current_status": "ACTIVATED",
  "current_owner": "Carrier_Node_A",
  "is_tampered": false,
  "lifecycle_history": [
    { "block_index": 1, "event": "REGISTRATION", "owner": "OEM_ORIGIN" },
    { "block_index": 2, "event": "CUSTODY_TRANSFER", "owner": "Carrier_Node_A" }
  ]
}

### 2. The Operational Control Tower UI (Streamlit Dashboard)
- **Interface Access:** Accessible locally at http://localhost:8501[cite: 1]
- **Output Artifact:** A comprehensive web console displaying real-time hardware authenticity states[cite: 1]. It delivers:
  - **Authenticity Metric Blocks:** Displays green GENUINE or red ALERT: TAMPERED device security states[cite: 1].
  - **Live Analytical Telemetry:** Renders performance graphs verifying real-world KPIs, including Blacklist Propagation Speed maintaining an execution time of < 2 minutes globally across network peers[cite: 1].

### 3. Automated Security Simulation Logs (PyTest Matrix)
- **Interface Access:** Generated within the terminal via docker-compose run api-gateway pytest tests/[cite: 1]
- **Output Artifact:** Structured terminal output detailing defense evaluations[cite: 1]. When a simulated attack modifies a database cell directly, the validation engine outputs critical exception logs[cite: 1]:

telecom_api  | [SECURITY CRITICAL] Cryptographic hash mismatch detected for IMEI 359821061234567.[cite: 1]
telecom_api  | [ALERT] Local state hash does not match sequential blockchain block hash pointer![cite: 1]
telecom_api  | [ACTION] State flagged as TAMPERED. Log appended to immutable audit trail.[cite: 1]

---

## 📊 Core Performance Metrics

This architecture is built to meet high-throughput enterprise Service Level Agreements (SLAs) validated in production simulations[cite: 1]:
* **Blacklist Propagation Speed:** Reduced from a 24–48 hour legacy baseline down to < 2 minutes globally across connected carrier nodes[cite: 1].
* **Fraud Infiltration Mitigation:** Demonstrated a 52% to 65% reduction in fraudulent network activation attempts by blocking cloned identities at the API gateway[cite: 1].
* **Forensic Audit Auditing:** Network-wide supply chain tracing and device history audits reduced from days down to < 10 minutes[cite: 1].

---

## 🚀 Local Deployment and Orchestration

The entire infrastructure layer is virtualized using Docker container structures to simulate a local multi-region consensus network[cite: 1].

### Prerequisites
Ensure your local machine has Docker Desktop installed and running in the background[cite: 1].

### Initialization Command
Execute the compilation array from a terminal opened inside your root folder[cite: 1]:

docker-compose up --build