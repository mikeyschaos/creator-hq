import json
import os
import tempfile

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY not found in .env")

CHANNELS = {
    "I'd Dig It": "UCSDKMK8RCGHyjNvIfnYssVw",
    "Guns & Game": "UCW6SQjQozoEiYe2RfiKDhtQ",
    "Mikey's Chaos": "UC8V5_EWsCZzSOxOldl1D84w",
}

results = {}

for index, (name, channel_id) in enumerate(CHANNELS.items(), start=1):

    print(f"[{index}/{len(CHANNELS)}] Updating {name}")

    try:
        # -----------------------------
        # Channel Statistics
        # -----------------------------
        stats_response = requests.get(
            "https://www.googleapis.com/youtube/v3/channels",
            params={
                "part": "statistics",
                "id": channel_id,
                "key": API_KEY,
            },
            timeout=15,
        )

        stats_response.raise_for_status()

        stats_json = stats_response.json()

        if not stats_json.get("items"):
            raise RuntimeError("No statistics returned")

        statistics = stats_json["items"][0]["statistics"]

        print("   ✓ Statistics")

        # -----------------------------
        # Latest Upload
        # -----------------------------
        search_response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "channelId": channel_id,
                "order": "date",
                "type": "video",
                "maxResults": 1,
                "key": API_KEY,
            },
            timeout=15,
        )

        search_response.raise_for_status()

        search_json = search_response.json()

        latest_video = {}

        if search_json.get("items"):

            item = search_json["items"][0]

            latest_video = {
                "title": item["snippet"]["title"],
                "publishedAt": item["snippet"]["publishedAt"],
                "videoId": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            }

            print("   ✓ Latest Upload")

        results[name] = {
            "subscribers": int(statistics.get("subscriberCount", 0)),
            "views": int(statistics.get("viewCount", 0)),
            "videos": int(statistics.get("videoCount", 0)),
            "latestVideo": latest_video,
        }

    except Exception as exc:
        print(f"   ✗ {exc}")

EXPECTED_CHANNELS = len(CHANNELS)

if len(results) != EXPECTED_CHANNELS:
    print("\nERROR: Not all channels updated successfully.")
    print("Keeping existing youtube_data.json unchanged.")
    raise SystemExit(1)

os.makedirs("data", exist_ok=True)

tmp = tempfile.NamedTemporaryFile(
    mode="w",
    delete=False,
    dir="data",
)

json.dump(results, tmp, indent=2)

tmp.close()

os.replace(tmp.name, "data/youtube_data.json")

print("\n✓ YouTube data updated successfully.")
