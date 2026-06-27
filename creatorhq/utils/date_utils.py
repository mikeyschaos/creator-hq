"""
Creator HQ Date Utilities
"""

from datetime import datetime, timezone


def days_since(iso_date: str) -> int:
    """
    Returns the number of whole days since an ISO-8601 UTC timestamp.

    Example:
        2026-06-20T18:42:11Z
    """

    if not iso_date:
        return 0

    uploaded = datetime.strptime(
        iso_date,
        "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    return (now - uploaded).days


def upload_status(days: int):
    """
    Returns (color, message)
    """

    if days <= 7:
        return (
            "green",
            "On Track"
        )

    if days <= 14:
        return (
            "yellow",
            "Time to Plan"
        )

    return (
        "red",
        "Ready for Your Next Upload"
    )
