package main

import "testing"

func TestAllowedLifecycleTransitions(t *testing.T) {
	cases := [][2]string{{"REGISTERED", "DISTRIBUTOR_CUSTODY"}, {"DISTRIBUTOR_CUSTODY", "CARRIER_CUSTODY"}, {"CARRIER_CUSTODY", "ACTIVATED"}, {"ACTIVATED", "BLACKLISTED"}, {"BLACKLISTED", "DECOMMISSIONED"}}
	for _, c := range cases {
		if err := validateLifecycleTransition(c[0], c[1]); err != nil {
			t.Fatalf("expected %s -> %s to be allowed: %v", c[0], c[1], err)
		}
	}
}

func TestInvalidLifecycleTransitionRejected(t *testing.T) {
	if err := validateLifecycleTransition("ACTIVATED", "REGISTERED"); err == nil {
		t.Fatal("expected invalid transition to be rejected")
	}
	if err := validateLifecycleTransition("REGISTERED", "BANANA"); err == nil {
		t.Fatal("expected unknown state to be rejected")
	}
}

func TestTransitionAuthorization(t *testing.T) {
	if err := authorizeLifecycleTransition("CARRIER_CUSTODY", "ACTIVATED", "CarrierMSP"); err != nil {
		t.Fatal(err)
	}
	if err := authorizeLifecycleTransition("CARRIER_CUSTODY", "ACTIVATED", "DistributorMSP"); err == nil {
		t.Fatal("expected unauthorized MSP rejection")
	}
}
