import json
from datetime import datetime
from app.models.event import EconomicEvent

DATA_FILE = "app/data/economic_calendar.json"


def fetch_events():
    events = []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw_events = json.load(f)

    for e in raw_events:
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
