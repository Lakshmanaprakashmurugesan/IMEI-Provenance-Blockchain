package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct{ contractapi.Contract }

var allowedTransitions = map[string]map[string]bool{
	"REGISTERED":          {"DISTRIBUTOR_CUSTODY": true},
	"DISTRIBUTOR_CUSTODY": {"CARRIER_CUSTODY": true},
	"CARRIER_CUSTODY":     {"ACTIVATED": true},
	"ACTIVATED":           {"BLACKLISTED": true, "DECOMMISSIONED": true},
	"BLACKLISTED":         {"DECOMMISSIONED": true},
}

var transitionMSP = map[string]string{
	"REGISTERED->DISTRIBUTOR_CUSTODY":      "OEMMSP",
	"DISTRIBUTOR_CUSTODY->CARRIER_CUSTODY": "DistributorMSP",
	"CARRIER_CUSTODY->ACTIVATED":           "CarrierMSP",
	"ACTIVATED->BLACKLISTED":               "CarrierMSP",
	"ACTIVATED->DECOMMISSIONED":            "CarrierMSP",
	"BLACKLISTED->DECOMMISSIONED":          "CarrierMSP",
}

func validateLifecycleTransition(currentStatus, newStatus string) error {
	next, ok := allowedTransitions[currentStatus]
	if !ok || !next[newStatus] {
		return fmt.Errorf("invalid lifecycle transition: %s -> %s", currentStatus, newStatus)
	}
	return nil
}

func authorizeLifecycleTransition(currentStatus, newStatus, callerMSP string) error {
	if err := validateLifecycleTransition(currentStatus, newStatus); err != nil {
		return err
	}
	required := transitionMSP[currentStatus+"->"+newStatus]
	if required == "" || callerMSP != required {
		return fmt.Errorf("MSP %s is not authorized for lifecycle transition %s -> %s", callerMSP, currentStatus, newStatus)
	}
	return nil
}

func callerMSP(ctx contractapi.TransactionContextInterface) (string, error) {
	mspID, err := ctx.GetClientIdentity().GetMSPID()
	if err != nil {
		return "", fmt.Errorf("unable to resolve client MSP identity: %v", err)
	}
	return mspID, nil
}

func (s *SmartContract) RegisterDevice(ctx contractapi.TransactionContextInterface, imei string, fingerprint string) error {
	mspID, err := callerMSP(ctx)
	if err != nil {
		return err
	}
	if mspID != "OEMMSP" {
		return fmt.Errorf("only OEMMSP may register a device; caller=%s", mspID)
	}
	exists, err := s.AssetExists(ctx, imei)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("device identifier %s already exists on the ledger", imei)
	}
	txID := ctx.GetStub().GetTxID()
	ts, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return err
	}
	event := LifecycleEvent{TxID: txID, Timestamp: ts.AsTime().String(), Event: "REGISTRATION_GENESIS", Operator: mspID}
	asset := DeviceProvenanceAsset{IMEI: imei, CurrentStatus: "REGISTERED", CurrentOwner: mspID, LastUpdatedBy: mspID, AsymmetricFinger: fingerprint, LifecycleHistory: []LifecycleEvent{event}}
	b, err := json.Marshal(asset)
	if err != nil {
		return err
	}
	return ctx.GetStub().PutState(imei, b)
}

// TransferCustody changes both lifecycle state and current owner. Caller identity is derived from Fabric MSP.
func (s *SmartContract) TransferCustody(ctx contractapi.TransactionContextInterface, imei, newOwnerMSP, newStatus string) error {
	asset, err := s.QueryDevice(ctx, imei)
	if err != nil {
		return err
	}
	mspID, err := callerMSP(ctx)
	if err != nil {
		return err
	}
	if err := authorizeLifecycleTransition(asset.CurrentStatus, newStatus, mspID); err != nil {
		return err
	}
	if asset.CurrentOwner != mspID {
		return fmt.Errorf("caller MSP %s does not own current custody; current owner=%s", mspID, asset.CurrentOwner)
	}
	txID := ctx.GetStub().GetTxID()
	ts, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return err
	}
	event := LifecycleEvent{TxID: txID, Timestamp: ts.AsTime().String(), Event: newStatus, Operator: mspID}
	asset.CurrentStatus = newStatus
	asset.CurrentOwner = newOwnerMSP
	asset.LastUpdatedBy = mspID
	asset.LifecycleHistory = append(asset.LifecycleHistory, event)
	b, err := json.Marshal(asset)
	if err != nil {
		return err
	}
	return ctx.GetStub().PutState(imei, b)
}

// UpdateDeviceStatus applies a non-custody lifecycle transition using the authenticated Fabric MSP identity.
func (s *SmartContract) UpdateDeviceStatus(ctx contractapi.TransactionContextInterface, imei, newStatus string) error {
	asset, err := s.QueryDevice(ctx, imei)
	if err != nil {
		return err
	}
	mspID, err := callerMSP(ctx)
	if err != nil {
		return err
	}
	if err := authorizeLifecycleTransition(asset.CurrentStatus, newStatus, mspID); err != nil {
		return err
	}
	if asset.CurrentOwner != mspID {
		return fmt.Errorf("caller MSP %s does not own current custody; current owner=%s", mspID, asset.CurrentOwner)
	}
	txID := ctx.GetStub().GetTxID()
	ts, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return err
	}
	event := LifecycleEvent{TxID: txID, Timestamp: ts.AsTime().String(), Event: newStatus, Operator: mspID}
	asset.CurrentStatus = newStatus
	asset.LastUpdatedBy = mspID
	asset.LifecycleHistory = append(asset.LifecycleHistory, event)
	b, err := json.Marshal(asset)
	if err != nil {
		return err
	}
	return ctx.GetStub().PutState(imei, b)
}

func (s *SmartContract) QueryDevice(ctx contractapi.TransactionContextInterface, imei string) (*DeviceProvenanceAsset, error) {
	b, err := ctx.GetStub().GetState(imei)
	if err != nil {
		return nil, fmt.Errorf("failed reading world state: %v", err)
	}
	if b == nil {
		return nil, fmt.Errorf("device %s does not exist on this ledger", imei)
	}
	var asset DeviceProvenanceAsset
	if err := json.Unmarshal(b, &asset); err != nil {
		return nil, err
	}
	return &asset, nil
}

func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, imei string) (bool, error) {
	b, err := ctx.GetStub().GetState(imei)
	if err != nil {
		return false, err
	}
	return b != nil, nil
}

func main() {
	cc, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		panic(fmt.Sprintf("Error building chaincode: %v", err))
	}
	if err = cc.Start(); err != nil {
		panic(fmt.Sprintf("Error starting chaincode: %v", err))
	}
}
