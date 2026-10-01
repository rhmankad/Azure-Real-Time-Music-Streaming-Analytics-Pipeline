import json
import random
import uuid
from datetime import datetime, timezone

devices = ["iOS", "Android", "Web", "Desktop"]
countries = ["IN", "US", "GB", "CA", "DE"]
songs = [
    {"song_id": "S101", "artist_id": "A01", "track": "Midnight Drive"},
    {"song_id": "S102", "artist_id": "A02", "track": "Golden Horizon"},
    {"song_id": "S103", "artist_id": "A03", "track": "Urban Beats"},
    {"song_id": "S104", "artist_id": "A01", "track": "Echoes in Rain"}
]

events = []
for _ in range(50):
    selected_song = random.choice(songs)
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": f"USR_{random.randint(1000, 1050)}",
        "song_id": selected_song["song_id"],
        "artist_id": selected_song["artist_id"],
        "track_name": selected_song["track"],
        "stream_duration_sec": random.randint(10, 240),
        "device_type": random.choice(devices),
        "country": random.choice(countries),
        "event_timestamp": datetime.now(timezone.utc).isoformat()
    }
    events.append(event)

with open("C:/Users/ADMIN/Downloads/raw_streaming_events.json", "w") as f:
    for entry in events:
        f.write(json.dumps(entry) + "\n")

       