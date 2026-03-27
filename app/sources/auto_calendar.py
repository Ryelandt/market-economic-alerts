import os
import json
import urllib.parse
import urllib.request
from datetime import datetime, date, time, timedelta, timezone
from app.models.event import EconomicEvent

FRED_BASE_URL = "https://api.stlouisfed.org/fred/releases"

PARIS_TZ = timezone(timedelta(hours=1))


def fetch_events():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("FRED_API_KEY not set")
        return []

    params = {
        "api_key": api_key,
        "file_type": "json",
        "limit": 50
    }

    url = f"{FRED_BASE_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print("FRED API error:", e)
        return []

    today = date.today()
    events = []

    for r in data.get("releases", []):
        name = r.get("name", "")

        # Mapping annonce → heure de publication
        if "Consumer Price Index" in name:
            event_time = time(14, 30)
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
            importance = 3

        elif "Employment Situation" in name:
            event_time = time(14, 30)
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
            importance = 3

        else:
            continue  # bruit ignoré

        event_datetime = datetime.combine(today, event_time, PARIS_TZ)

        events.append(
            EconomicEvent(
                name=name,
                datetime=event_datetime,
                country="US",
                importance=importance,
                forecast=None,
                actual=None,
                affected_assets=assets
            )
        )

    return events
