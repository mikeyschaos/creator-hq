import json
import random
import os
from datetime import datetime

BASE_DIR = "/home/bigloot/dashboard"

STATS_FILE = os.path.join(BASE_DIR, "data", "stats.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "dashboard_data.json")
TIP_FILE = os.path.join(BASE_DIR, "tips", "creator_tips.txt")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def load_stats():
    with open(STATS_FILE, "r") as f:
        return json.load(f)


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def load_tip():
    with open(TIP_FILE, "r") as f:
        tips = [line.strip() for line in f if line.strip()]

    day = datetime.now().timetuple().tm_yday
    random.seed(day)

    return random.choice(tips)


def next_goal(channel_name, subscribers, goals):

    if channel_name in goals:
        return goals[channel_name]

    milestones = [
        100,
        250,
        500,
        1000,
        2500,
        5000,
        10000,
        25000,
        50000,
        100000
    ]

    for goal in milestones:
        if subscribers < goal:
            return goal

    return milestones[-1]


def build_dashboard():

    stats = load_stats()
    config = load_config()

    goals = config.get("goals", {})

    dashboard = {
        "generated": datetime.now().isoformat(),
        "creatorTip": load_tip(),
        "channels": [],
        "network": {},
        "settings": config.get("dashboard", {})
    }

    total_subs = 0
    total_views = 0
    total_videos = 0

    for channel_name, channel in stats.items():

        subs = int(channel["subscribers"])
        views = int(channel["views"])
        videos = int(channel["videos"])

        goal = next_goal(channel_name, subs, goals)

        dashboard["channels"].append({

            "name": channel_name,

            "subscribers": subs,

            "views": views,

            "videos": videos,

            "goal": goal,

            "remaining": goal - subs,

            "progress": round((subs / goal) * 100, 1)

        })

        total_subs += subs
        total_views += views
        total_videos += videos

    dashboard["network"] = {

        "subscribers": total_subs,

        "views": total_views,

        "videos": total_videos,

        "goal": config.get("networkGoal", 1000),

        "progress": round(
            (total_subs / config.get("networkGoal", 1000)) * 100,
            1
        )

    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)

    print("Dashboard data generated successfully.")


if __name__ == "__main__":
    build_dashboard()
