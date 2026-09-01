package main

import "testing"

func TestValidLifecycleTransitions(t *testing.T) {
	cases := [][2]string{
		{"REGISTERED", "DISTRIBUTOR_CUSTODY"},
		{"DISTRIBUTOR_CUSTODY", "CARRIER_CUSTODY"},
		{"CARRIER_CUSTODY", "ACTIVATED"},
		{"ACTIVATED", "BLACKLISTED"},
		{"ACTIVATED", "DECOMMISSIONED"},
		{"ACTIVATED", "DECOMMISSIONED"},
	}

	for _, c := range cases {
		if err := validateLifecycleTransition(c[0], c[1]); err != nil {
			t.Fatalf("expected %s -> %s valid: %v", c[0], c[1], err)
		}
	}
}

func TestInvalidLifecycleTransition(t *testing.T) {
	if err := validateLifecycleTransition("REGISTERED", "BANANA"); err == nil {
		t.Fatal("expected invalid transition rejection")
	}

	if err := validateLifecycleTransition("ACTIVATED", "REGISTERED"); err == nil {
		t.Fatal("expected reverse lifecycle transition rejection")
	}
}