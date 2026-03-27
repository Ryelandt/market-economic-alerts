import json
import urllib.request
from datetime import datetime
from app.models.event import EconomicEvent

API_URL = "https://API_CALENDAR_URL_HERE"  # ex: Trading Economics / OHLC / Fin2Dev


def fetch_trader_events():
    events = []

    with urllib.request.urlopen(API_URL, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    for e in data:
        events.append(
            EconomicEvent(
                name=e["name"],                 # "US CPI"
                datetime=datetime.fromisoformat(e["datetime"]),  # 2026-03-27T14:30:00
                country=e["country"],           # "US"
                importance=e["importance"],     # 3 = High
                forecast=e.get("consensus"),
                actual=e.get("actual"),
                affected_assets=e["assets"]     # ["EURUSD","XAUUSD"]
            )
        )

    return events
