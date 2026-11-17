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

# Additional test cases so every decision evaluates to both True and False (branch coverage).

# ---------- overage_charge ----------
def test_loyal_premium_gets_no_bonus():
    # premium is excluded from the loyalty bonus: 10 GB included, 11 GB used -> 1 GB extra at 15
    assert overage_charge("premium", 11, False, True) == 15

def test_not_loyal_no_bonus():
    # basic without loyalty: 2 GB included, 3 GB used -> 1 GB extra at 15
    assert overage_charge("basic", 3, False, False) == 15

def test_home_overage_heavy():
    # extra > 10 but not roaming: rate 15 + 10 = 25, no roaming surcharge
    assert overage_charge("standard", 20, False, False) == 15 * 25

def test_roaming_overage_small():
    # roaming with extra <= 10: flat roaming rate 40
    assert overage_charge("premium", 12, True, False) == 2 * 40

def test_exactly_included_boundary():
    # extra == 0 takes the "extra <= 0" branch
    assert overage_charge("premium", 10, True, False) == 0

def test_extra_exactly_ten_boundary():
    # extra == 10 is not > 10, so no heavy-usage surcharge
    assert overage_charge("basic", 12, False, False) == 10 * 15

def test_zero_usage_allowed():
    assert overage_charge("basic", 0, False, False) == 0

# ---------- recharge_allowed ----------
def test_recharge_kyc_pending_over_limit():
    assert recharge_allowed(201, 0, True) is False

def test_recharge_kyc_pending_boundary():
    assert recharge_allowed(200, 5, True) is True

def test_recharge_amount_boundary():
    assert recharge_allowed(2000, 2, False) is True

def test_recharge_too_many_pending():
    assert recharge_allowed(500, 3, False) is False

# ---------- validity_status ----------
def test_validity_postpaid_active():
    # postpaid, no addon: cutoff 3
    assert validity_status(3, False, False) == "active"

def test_validity_postpaid_grace():
    assert validity_status(2, False, False) == "grace"

def test_validity_prepaid_addon_active():
    # prepaid cutoff 0 + addon 2 = 2
    assert validity_status(2, True, True) == "active"

def test_validity_grace_boundary():
    # prepaid cutoff 0, grace down to -15
    assert validity_status(-15, True, False) == "grace"

def test_validity_expired_boundary():
    assert validity_status(-16, True, False) == "expired"
