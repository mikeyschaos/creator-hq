import json
import os
import random
import sys
from datetime import datetime

# --------------------------------------------------
# Allow imports from the Creator HQ project
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from creatorhq.utils.date_utils import (
    days_since,
    upload_status,
    format_elapsed,
)

from creatorhq.services.coach import build_coach_message

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

YOUTUBE_DATA_FILE = os.path.join(DATA_DIR, "youtube_data.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "dashboard_data.json")

TIP_FILE = os.path.join(PROJECT_ROOT, "tips", "creator_tips.txt")
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")


# --------------------------------------------------
# Loaders
# --------------------------------------------------

def load_youtube_data():
    with open(YOUTUBE_DATA_FILE, "r") as f:
        return json.load(f)


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def load_tip():
    with open(TIP_FILE, "r") as f:
        tips = [line.strip() for line in f if line.strip()]

    random.seed(datetime.now().timetuple().tm_yday)
    return random.choice(tips)


# --------------------------------------------------
# Goal Logic
# --------------------------------------------------

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
        100000,
    ]

    for goal in milestones:
        if subscribers < goal:
            return goal

    return milestones[-1]


# --------------------------------------------------
# Dashboard Builder
# --------------------------------------------------

def build_dashboard():

    youtube = load_youtube_data()
    config = load_config()

    goals = config.get("goals", {})

    dashboard = {
        "generated": datetime.now().isoformat(),
        "creatorTip": load_tip(),
        "channels": [],
        "network": {},
        "settings": config.get("dashboard", {}),
    }

    total_subscribers = 0
    total_views = 0
    total_videos = 0

    for channel_name, channel in youtube.items():

        subscribers = int(channel.get("subscribers", 0))
        views = int(channel.get("views", 0))
        videos = int(channel.get("videos", 0))

        latest_video = channel.get("latestVideo", {})

        published = latest_video.get("publishedAt")

        if published:
            days = days_since(published)
            color, message = upload_status(days)
            display = format_elapsed(days)
        else:
            days = None
            color = "gray"
            message = "No uploads found"
            display = "Never"

        goal = next_goal(channel_name, subscribers, goals)

        dashboard["channels"].append(
            {
                "name": channel_name,
                "subscribers": subscribers,
                "views": views,
                "videos": videos,
                "goal": goal,
                "remaining": goal - subscribers,
                "progress": round((subscribers / goal) * 100, 1),

                "latestVideo": latest_video,

                "uploadHealth": {
                    "daysSince": days,
                    "display": display,
                    "color": color,
                    "message": message,
                },
            }
        )

        total_subscribers += subscribers
        total_views += views
        total_videos += videos

    # -----------------------------
    # Coach's Corner
    # -----------------------------

    dashboard["coach"] = build_coach_message(
        dashboard["channels"]
    )

    network_goal = config.get("networkGoal", 1000)

    dashboard["network"] = {
        "subscribers": total_subscribers,
        "views": total_views,
        "videos": total_videos,
        "goal": network_goal,
        "progress": round((total_subscribers / network_goal) * 100, 1),
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)

    print("✓ Dashboard data generated successfully.")


if __name__ == "__main__":
    build_dashboard()
