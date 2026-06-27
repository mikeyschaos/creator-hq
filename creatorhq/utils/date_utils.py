"""
Creator HQ Date Utilities
"""

from datetime import datetime, timezone


def days_since(iso_date: str) -> int:
    """
    Returns the number of whole days since an ISO-8601 UTC timestamp.
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
        return ("green", "On Track")

    if days <= 14:
        return ("yellow", "Time to Plan")

    return ("red", "Ready for Your Next Upload")


def format_elapsed(days: int) -> str:
    """
    Converts elapsed days into a human-friendly string.

    Examples:
        3 days ago
        18 days ago
        2 months ago
        11 months ago
        1.3 years ago
        5.4 years ago
    """

    if days < 0:
        return "Today"

    if days == 0:
        return "Today"

    if days == 1:
        return "1 day ago"

    if days <= 30:
        return f"{days} days ago"

    if days < 365:
        months = round(days / 30)

        if months == 1:
            return "1 month ago"

        return f"{months} months ago"

    years = round(days / 365, 1)

    if years == 1:
        return "1 year ago"

    return f"{years} years ago"
