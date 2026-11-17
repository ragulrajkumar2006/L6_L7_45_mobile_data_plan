import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status

# Example test cases:
def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0

def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True

# Test cases written to execute every line of mobile_data_plan.py (line coverage).

# ---------- overage_charge ----------
def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)

def test_negative_usage_raises():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)

def test_loyal_non_premium_gets_bonus_gb():
    # basic: 2 GB + 1 loyalty GB = 3 GB included, so 3 GB used is free
    assert overage_charge("basic", 3, False, True) == 0

def test_home_overage_small():
    # standard: 5 GB included, 8 GB used -> 3 GB extra at 15/GB
    assert overage_charge("standard", 8, False, False) == 45

def test_roaming_overage_heavy():
    # basic: 2 GB included, 15 GB used -> 13 GB extra, roaming rate 40 + 10 + 5 = 55
    assert overage_charge("basic", 15, True, False) == 13 * 55

# ---------- recharge_allowed ----------
def test_recharge_kyc_pending():
    assert recharge_allowed(150, 0, True) is True

def test_recharge_amount_too_large():
    assert recharge_allowed(2500, 0, False) is False

# ---------- validity_status ----------
def test_validity_prepaid_active():
    assert validity_status(5, True, False) == "active"

def test_validity_postpaid_addon_grace():
    # postpaid cutoff 3 + addon 2 = 5; 0 days left is within grace (>= -10)
    assert validity_status(0, False, True) == "grace"

def test_validity_expired():
    assert validity_status(-20, True, False) == "expired"
