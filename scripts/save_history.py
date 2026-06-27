import json
import os
import shutil
from datetime import datetime

STATS_FILE = "/home/bigloot/creator-hq/data/youtube_data.json"
HISTORY_DIR = "/home/bigloot/dashboard/history"

os.makedirs(HISTORY_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

history_file = os.path.join(
    HISTORY_DIR,
    f"{timestamp}.json"
)

# Copy the file directly instead of loading/rewriting JSON
shutil.copy2(STATS_FILE, history_file)

print(f"History saved: {history_file}")
