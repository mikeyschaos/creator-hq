"""
Creator HQ
Coach's Corner Service

Chooses the single most important coaching message
to display on the dashboard.
"""


def build_coach_message(channels):
    """
    Returns a dictionary containing the coach message.

    Parameters
    ----------
    channels : list
        dashboard["channels"]

    Returns
    -------
    dict
    """

    if not channels:
        return {
            "icon": "💡",
            "title": "Coach's Corner",
            "message": "No channel data available."
        }

    # --------------------------------------------------
    # Priority 1
    # Longest time since upload
    # --------------------------------------------------

    oldest = max(
        channels,
        key=lambda c: c["uploadHealth"]["daysSince"] or 0
    )

    days = oldest["uploadHealth"]["daysSince"]

    if days >= 365:

        years = round(days / 365, 1)

        return {
            "icon": "🎯",
            "title": "Coach's Corner",
            "message":
                f"{oldest['name']} hasn't had a new upload in "
                f"{years} years.\n\n"
                "One upload could completely change your momentum."
        }

    # --------------------------------------------------
    # Priority 2
    # Closest milestone
    # --------------------------------------------------

    closest = min(
        channels,
        key=lambda c: c["remaining"]
    )

    return {
        "icon": "🚀",
        "title": "Coach's Corner",
        "message":
            f"{closest['name']} is only "
            f"{closest['remaining']} subscribers away "
            f"from its next goal."
    }
