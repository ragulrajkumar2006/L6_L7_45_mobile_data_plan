import math


def _to_number(text):
    # float() accepts "nan", "inf" and overflows like "1e309" to inf; reject those too.
    try:
        value = float(text)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(value):
        return None
    return value


def parse_plan(text):
    # Returns (plan, gb), or None if the input is not "plan:gb" with a name and gb >= 0.
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    plan, gb = text.split(':')
    plan = plan.strip()
    gb = _to_number(gb)
    if not plan or gb is None or gb < 0:
        return None
    return plan.title(), gb


def usage_average(usage_csv):
    # Returns the mean daily usage, or None unless every entry is a whole number >= 0.
    if not isinstance(usage_csv, str):
        return None
    try:
        values = [int(r) for r in usage_csv.split(',')]
    except ValueError:  # also covers empty entries and ints too long to convert
        return None
    if any(v < 0 for v in values):
        return None
    return sum(values) / len(values)


def payable_bill(text):
    # Returns bill + 18% tax - discount (never below 0), or None for invalid input.
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    bill, discount = (_to_number(part) for part in text.split('|'))
    if bill is None or discount is None or bill < 0 or discount < 0:
        return None
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        return None
    return round(max(total, 0), 2)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    print("Plan and Data:", result if result is not None else "Invalid input")

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    print("Average Usage:", result if result is not None else "Invalid input")

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
