# Prototype Validation Summary

## Current Python validation

Command:

```text
python run\_validation.py
```

Current result in this enhancement environment:

```text
9 passed
```

The generated machine-readable result is `evidence/pytest\_results.xml`; console output is in `evidence/pytest\_console\_output.txt`.

## What the Python tests validate

1. Generated synthetic IMEIs pass format/check-digit validation.
2. Four-state classification behaves as GENUINE / TAMPERED / UNKNOWN / INVALID without hardcoded IMEI decision rules.
3. ECDSA P-256 manufacturer signatures are genuinely verified and fail after payload modification.
4. AES-256-GCM encrypt/decrypt works and tampered ciphertext fails authentication.
5. Off-chain encrypted content is actually persisted to disk and can be restored with the correct key.
6. API and shared provenance engine return the same authenticity result.
7. Event-stream code is explicitly labeled simulation (`SIMULATED\_EMIT` / `SIMULATED\_PROCESS`) and the dashboard evidence path executes producer → consumer simulation code.
8. The API returns the shared `INVALID` state rather than maintaining a separate malformed-IMEI decision path.
9. `UNKNOWN` is explicitly neither genuine nor tampered.

## Go chaincode validation note

The Go unit-test source includes lifecycle transition rules, and go test ./... now executes successfully in the current environment with the required Hyperledger Fabric dependency available. This confirms that the Go test suite can be executed successfully. The repository should still be characterized as Fabric-oriented chaincode and test implementation rather than as evidence of a deployed Hyperledger Fabric network.

## Streamlit startup note

The enhancement execution container did not have the `streamlit` package installed, so the UI server was not claimed as runtime-tested here. `dashboard/app.py` was Python syntax-checked successfully. On the target Windows environment, install `requirements.txt` and run the commands in `How to execute.txt`.

## Evidence integrity

Historical generated logs and sample artifacts from the pre-enhancement build were moved to `evidence/legacy/` rather than deleted or rewritten. Current runtime logs start with clean schemas and should be populated by actual executions of the enhanced prototype.

