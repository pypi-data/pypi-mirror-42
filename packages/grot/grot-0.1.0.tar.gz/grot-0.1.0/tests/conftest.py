from grot import string_types


def pytest_assertrepr_compare(op, left, right):
    if op == "==" and isinstance(left, string_types) and isinstance(right, string_types):
        if len(left) > 10 or len(right) > 10:
            print("--- (left):")
            print(left)
            print("---")
            print("does not match currently defined reference:")
            print("--- (right):")
            print(right)
            print("---")
