import json
import urllib.request
from datetime import datetime
from app.models.event import EconomicEvent

API_URL = "https://example.com/api/economic-calendar"


def fetch_events():
    events = []

    with urllib.request.urlopen(API_URL, timeout=10) as response:
        raw_data = json.loads(response.read().decode("utf-8"))

    for e in raw_data:
        events.append(
            EconomicEvent(
                name=e["name"],
                datetime=datetime.fromisoformat(e["datetime"]),
                country=e["country"],
                importance=e["importance"],
                forecast=e.get("forecast"),
                actual=e.get("actual"),
                affected_assets=e["affected_assets"]
            )
        )

    return events
