# Prototype Validation Summary

## Current Python validation

Command:

```text
python run_validation.py
```

Current result in this enhancement environment:

```text
9 passed
```

The generated machine-readable result is `evidence/pytest_results.xml`; console output is in `evidence/pytest_console_output.txt`.

## What the Python tests validate

1. Generated synthetic IMEIs pass format/check-digit validation.
2. Four-state classification behaves as GENUINE / TAMPERED / UNKNOWN / INVALID without hardcoded IMEI decision rules.
3. ECDSA P-256 manufacturer signatures are genuinely verified and fail after payload modification.
4. AES-256-GCM encrypt/decrypt works and tampered ciphertext fails authentication.
5. Off-chain encrypted content is actually persisted to disk and can be restored with the correct key.
6. API and shared provenance engine return the same authenticity result.
7. Event-stream code is explicitly labeled simulation (`SIMULATED_EMIT` / `SIMULATED_PROCESS`) and the dashboard evidence path executes producer → consumer simulation code.
8. The API returns the shared `INVALID` state rather than maintaining a separate malformed-IMEI decision path.
9. `UNKNOWN` is explicitly neither genuine nor tampered.

## Go chaincode validation note

A Go unit-test source is included for lifecycle transition rules. In the enhancement execution environment, `go test ./...` could not download `github.com/hyperledger/fabric-contract-api-go` because outbound access to `proxy.golang.org` was blocked. This is an environment dependency-fetch limitation; it is **not represented as a passing Go test** in this evidence package. Run the command in a normal networked Go environment before independent review and preserve the resulting output.

## Streamlit startup note

The enhancement execution container did not have the `streamlit` package installed, so the UI server was not claimed as runtime-tested here. `dashboard/app.py` was Python syntax-checked successfully. On the target Windows environment, install `requirements.txt` and run the commands in `How to execute.txt`.

## Evidence integrity

Historical generated logs and sample artifacts from the pre-enhancement build were moved to `evidence/legacy/` rather than deleted or rewritten. Current runtime logs start with clean schemas and should be populated by actual executions of the enhanced prototype.
