package main

// DeviceProvenanceAsset represents the immutable identity profile of a mobile device on the ledger.
type DeviceProvenanceAsset struct {
	IMEI             string           `json:"imei"`
	CurrentStatus    string           `json:"current_status"` // REGISTRATION, TRANSFER, ACTIVATION, BLACKLIST
	CurrentOwner     string           `json:"current_owner"`  // The current carrier or distributor MSP ID
	LastUpdatedBy    string           `json:"last_updated_by"`
	AsymmetricFinger string           `json:"public_key_fingerprint"`
	LifecycleHistory []LifecycleEvent `json:"lifecycle_history"`
}

// LifecycleEvent logs chronological ledger modifications for forensic audit tracking.
type LifecycleEvent struct {
	TxID      string `json:"tx_id"`
	Timestamp string `json:"timestamp"`
	Event     string `json:"event"`
	Operator  string `json:"operator"`
}
