import requests
import json
from feedgen.feed import FeedGenerator
from datetime import datetime

models = [
"onlyems23",
"fiery_redhead"
]

STATE_FILE = "state.json"
RSS_FILE = "feed.xml"

try:
    with open(STATE_FILE) as f:
        state = json.load(f)
except:
    state = {}

fg = FeedGenerator()
fg.title("Chaturbate Live Alerts")
fg.link(href="https://chaturbate.com")

new_entries = False

for username in models:

    url = f"https://chaturbate.com/api/room_status/?room={username}"

    try:
        data = requests.get(url).json()
        status = data["room_status"]
    except:
        status = "offline"

    last = state.get(username, "offline")

    if status == "public" and last != "public":

        entry = fg.add_entry()
        entry.title(f"{username} is LIVE")
        entry.link(href=f"https://chaturbate.com/{username}/")
        entry.pubDate(datetime.utcnow())

        new_entries = True

    state[username] = status

if new_entries:
    fg.rss_file(RSS_FILE)

with open(STATE_FILE, "w") as f:
    json.dump(state, f)
