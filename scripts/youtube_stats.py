import requests
import json
import tempfile
import os

API_KEY = " AIzaSyAxnX-1yaJxqBOM5yo-bpKiyfGrf-A_akI"

CHANNELS = {
    "I'd Dig It": "UCSDKMK8RCGHyjNvIfnYssVw",
    "Guns & Game": "UCW6SQjQozoEiYe2RfiKDhtQ",
    "Mikey's Chaos": "UC8V5_EWsCZzSOxOldl1D84w"
}

results = {}

for name, channel_id in CHANNELS.items():

    print(f"Updating {name}")

    url = (
        "https://www.googleapis.com/youtube/v3/channels"
        f"?part=statistics&id={channel_id}&key={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data.get("items"):
            print(f"ERROR: No data returned for {name}")
            continue

        stats = data["items"][0]["statistics"]

        results[name] = {
            "subscribers": stats.get("subscriberCount", "0"),
            "views": stats.get("viewCount", "0"),
            "videos": stats.get("videoCount", "0")
        }

    except Exception as e:
        print(f"ERROR updating {name}: {e}")

# Safety check
EXPECTED_CHANNELS = len(CHANNELS)

if len(results) != EXPECTED_CHANNELS:
    print(
        f"\nERROR: Expected {EXPECTED_CHANNELS} channels but only received {len(results)}."
    )
    print("Keeping existing youtube_data.json unchanged.")
    raise SystemExit(1)

# Atomic write
os.makedirs("data", exist_ok=True)

tmp = tempfile.NamedTemporaryFile(
    mode="w",
    delete=False,
    dir="data"
)

json.dump(results, tmp, indent=2)

tmp.close()

os.replace(tmp.name, "data/youtube_data.json")

print("\nStats updated successfully")
