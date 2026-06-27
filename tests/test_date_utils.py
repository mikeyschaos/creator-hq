"""
Creator HQ
Date Utility Tests
"""

from creatorhq.utils.date_utils import (
    days_since,
    upload_status,
    format_elapsed,
)


def run_tests():

    print("Running date utility tests...\n")

    print("Test 1: Upload Status")

    assert upload_status(3)[0] == "green"
    assert upload_status(10)[0] == "yellow"
    assert upload_status(20)[0] == "red"

    print("✓ Upload status tests passed")

    print()

    print("Test 2: Days Since")

    days = days_since("2026-06-20T18:42:11Z")

    assert isinstance(days, int)

    print(f"✓ Days since returned integer ({days})")

    print()

    print("Test 3: Friendly Dates")

    assert format_elapsed(0) == "Today"
    assert format_elapsed(1) == "1 day ago"
    assert format_elapsed(5) == "5 days ago"
    assert format_elapsed(45) == "2 months ago"
    assert format_elapsed(400) == "1.1 years ago"

    print("✓ Friendly date formatting passed")

    print()

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
