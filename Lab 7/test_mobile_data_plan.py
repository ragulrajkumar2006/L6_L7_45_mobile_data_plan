import math

from hypothesis import given, strategies as st
from mobile_data_plan import parse_plan, usage_average, payable_bill

# Numbers as text, including the awkward ones: negatives, nan, inf, huge, junk.
number_text = (
    st.integers().map(str)
    | st.floats().map(str)
    | st.sampled_from(["nan", "inf", "-inf", "1e309", "", " ", "abc", "1_000"])
)


# ---------- parse_plan ----------
@given(st.text() | st.none())
def test_parse_plan_no_crash(s):
    try:
        parse_plan(s)
    except Exception as e:
        assert False, f"parse_plan crashed with: {e!r}"

@given(st.text(), number_text)
def test_parse_plan_gb_is_valid(plan, gb):
    # Any accepted result must have a non-empty plan name and finite, non-negative GB.
    try:
        result = parse_plan(f"{plan}:{gb}")
    except Exception as e:
        assert False, f"parse_plan crashed with: {e!r}"
    if result is not None:
        name, data = result
        assert name != ""
        assert math.isfinite(data) and data >= 0

@given(st.sampled_from(["basic", "standard", "premium"]), st.integers(0, 1000))
def test_parse_plan_valid_input(plan, gb):
    assert parse_plan(f" {plan} : {gb} ") == (plan.title(), float(gb))


# ---------- usage_average ----------
@given(st.text() | st.none())
def test_usage_average_no_crash(s):
    try:
        usage_average(s)
    except Exception as e:
        assert False, f"usage_average crashed with: {e!r}"

@given(st.lists(st.integers()))
def test_usage_average_lists_of_integers(values):
    # Empty lists and negative usage must be rejected, not crash or be averaged.
    try:
        result = usage_average(",".join(map(str, values)))
    except Exception as e:
        assert False, f"usage_average crashed with: {e!r}"
    if not values or min(values) < 0:
        assert result is None
    else:
        assert result == sum(values) / len(values)


# ---------- payable_bill ----------
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r}"

@given(number_text, number_text)
def test_payable_bill_is_finite_and_non_negative(bill, discount):
    try:
        result = payable_bill(f"{bill}|{discount}")
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result) and result >= 0

@given(st.integers(0, 10**6), st.integers(0, 10**6))
def test_payable_bill_never_exceeds_taxed_bill(bill, discount):
    # A discount can only lower the bill, never raise it.
    result = payable_bill(f"{bill}|{discount}")
    assert 0 <= result <= round(bill * 1.18, 2)
