# Lifecycle and MSP Authorization Rules

The Go chaincode uses Fabric client identity (`GetMSPID`) rather than trusting a caller-provided `operator` string.

| Current state | Next state | Required caller MSP |
|---|---|---|
| REGISTERED | DISTRIBUTOR_CUSTODY | OEMMSP |
| DISTRIBUTOR_CUSTODY | CARRIER_CUSTODY | DistributorMSP |
| CARRIER_CUSTODY | ACTIVATED | CarrierMSP |
| ACTIVATED | BLACKLISTED | CarrierMSP |
| ACTIVATED | DECOMMISSIONED | CarrierMSP |
| BLACKLISTED | DECOMMISSIONED | CarrierMSP |

`TransferCustody` records the authenticated caller MSP, changes the owner, and appends a lifecycle event. `UpdateDeviceStatus` applies non-custody transitions with the same MSP checks.
