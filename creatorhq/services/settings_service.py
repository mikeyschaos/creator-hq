"""
Creator HQ Settings Service

Handles reading and writing application configuration.
"""

import json
import os
import subprocess


class SettingsService:

    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")

    TIPS_FILE = os.path.join(
        PROJECT_ROOT,
        "tips",
        "creator_tips.txt",
    )

    DASHBOARD_ENGINE = os.path.join(
        PROJECT_ROOT,
        "scripts",
        "dashboard_engine.py",
    )

    @classmethod
    def load(cls):
        with open(cls.CONFIG_FILE, "r") as f:
            return json.load(f)

    @classmethod
    def save(cls, config):
        with open(cls.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def get_goals(cls):
        config = cls.load()

        return {
            "goals": config.get("goals", {}),
            "networkGoal": config.get("networkGoal", 1000),
        }

    @classmethod
    def save_goals(cls, goals, network_goal):
        config = cls.load()

        config["goals"] = goals
        config["networkGoal"] = int(network_goal)

        cls.save(config)
        cls.regenerate_dashboard()

    @classmethod
    def get_tips(cls):
        """
        Return all creator tips.
        """

        if not os.path.exists(cls.TIPS_FILE):
            return []

        with open(cls.TIPS_FILE, "r") as f:
            return [
                line.strip()
                for line in f
                if line.strip()
            ]

    @classmethod
    def save_tips(cls, tips):
        """
        Save creator tips.
        """

        with open(cls.TIPS_FILE, "w") as f:
            for tip in tips:
                tip = tip.strip()
                if tip:
                    f.write(tip + "\n")

        cls.regenerate_dashboard()

    @classmethod
    def regenerate_dashboard(cls):
        try:
            subprocess.run(
                ["python", cls.DASHBOARD_ENGINE],
                cwd=cls.PROJECT_ROOT,
                check=True,
            )
        except Exception as e:
            print(f"Dashboard regeneration failed: {e}")
