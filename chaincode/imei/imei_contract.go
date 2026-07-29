package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract defines the structural interface for asset provenance operations
type SmartContract struct {
	contractapi.Contract
}

// RegisterDevice registers a brand new 15-digit hardware identity to the ledger (Genesis block entry)
func (s *SmartContract) RegisterDevice(ctx contractapi.TransactionContextInterface, imei string, owner string, fingerprint string) error {
	// Check if asset already exists to prevent duplicate spoofing
	exists, err := s.AssetExists(ctx, imei)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("cryptographic identity clash: device identifier %s already exists on the ledger", imei)
	}

	txID := ctx.GetStub().GetTxID()
	txTimestamp, _ := ctx.GetStub().GetTxTimestamp()
	timeString := txTimestamp.AsTime().String()

	// Build the transaction event block
	event := LifecycleEvent{
		TxID:      txID,
		Timestamp: timeString,
		Event:     "REGISTRATION_GENESIS",
		Operator:  owner,
	}

	asset := DeviceProvenanceAsset{
		IMEI:             imei,
		CurrentStatus:    "REGISTERED",
		CurrentOwner:     owner,
		LastUpdatedBy:    owner,
		AsymmetricFinger: fingerprint,
		LifecycleHistory: []LifecycleEvent{event},
	}

	assetBytes, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	// Write permanently to state database
	return ctx.GetStub().PutState(imei, assetBytes)
}

// UpdateDeviceStatus transitions a device through its operational lifecycle gates
func (s *SmartContract) UpdateDeviceStatus(ctx contractapi.TransactionContextInterface, imei string, newStatus string, operator string) error {
	asset, err := s.QueryDevice(ctx, imei)
	if err != nil {
		return err
	}

	// Security Rule: If a device is already blacklisted, lockdown state is absolute
	if asset.CurrentStatus == "BLACKLIST" && newStatus != "REVOKED_DECOMMISSION" {
		return fmt.Errorf("security policy exception: asset %s is blacklisted and locked down", imei)
	}

	txID := ctx.GetStub().GetTxID()
	txTimestamp, _ := ctx.GetStub().GetTxTimestamp()
	timeString := txTimestamp.AsTime().String()

	// Append chronological event block
	newEvent := LifecycleEvent{
		TxID:      txID,
		Timestamp: timeString,
		Event:     newStatus,
		Operator:  operator,
	}

	asset.CurrentStatus = newStatus
	asset.LastUpdatedBy = operator
	asset.LifecycleHistory = append(asset.LifecycleHistory, newEvent)

	assetBytes, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(imei, assetBytes)
}

// QueryDevice retrieves the entire chronological transaction history for verification
func (s *SmartContract) QueryDevice(ctx contractapi.TransactionContextInterface, imei string) (*DeviceProvenanceAsset, error) {
	assetBytes, err := ctx.GetStub().GetState(imei)
	if err != nil {
		return nil, fmt.Errorf("failed reading state block from world state: %v", err)
	}
	if assetBytes == nil {
		return nil, fmt.Errorf("the hardware asset %s does not exist on this ledger node", imei)
	}

	var asset DeviceProvenanceAsset
	err = json.Unmarshal(assetBytes, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// AssetExists is an internal health check tracing device presence
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, imei string) (bool, error) {
	assetBytes, err := ctx.GetStub().GetState(imei)
	if err != nil {
		return false, err
	}
	return assetBytes != nil, nil
}

func main() {
	cc, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		panic(fmt.Sprintf("Error building imei provenance chaincode engine: %v", err))
	}
	if err = cc.Start(); err != nil {
		panic(fmt.Sprintf("Error activating permissioned consensus network interface: %v", err))
	}
}