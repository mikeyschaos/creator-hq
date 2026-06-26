"""
Creator HQ Dashboard Service

Combines live dashboard data with channel configuration.
"""

from pathlib import Path
import json

DATA_FILE = Path("data/dashboard_data.json")
CONFIG_FILE = Path("config/channels.json")


class DashboardService:

    @staticmethod
    def load():

        dashboard = {
            "generated": "Unknown",
            "creatorTip": "",
            "channels": [],
            "network": {
                "subscribers": 0,
                "views": 0,
                "videos": 0,
            },
        }

        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                dashboard = json.load(f)

        config = {}

        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)

        for channel in dashboard.get("channels", []):

            settings = config.get(channel["name"], {})

            channel["image"] = settings.get("image", "")
            channel["goal"] = settings.get("goal", 1000)
            channel["color"] = settings.get("color", "#666666")
            channel["youtube"] = settings.get("youtube", "")

        return dashboard
