import os
import json
import urllib.parse
import urllib.request
from datetime import datetime
from app.models.event import EconomicEvent

BASE_URL = "https://api.stlouisfed.org/fred/release/dates"


def fetch_events():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("FRED_API_KEY not set")
        return []

    params = {
        "api_key": api_key,
        "file_type": "json",
        "limit": 15
    }

    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print("FRED API error:", e)
        return []

    events = []

    for r in data.get("release_dates", []):
        name = r["release_name"]
        date_str = r["date"]

        # Exemple de mapping simple vers actifs
        assets = []
        if "Consumer Price Index" in name:
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
        elif "Employment Situation" in name:
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
        else:
            continue  # ignore le reste pour le moment

        events.append(
            EconomicEvent(
                name=name,
                datetime=datetime.fromisoformat(date_str),
                country="US",
                importance=3,
                forecast=None,
                actual=None,
                affected_assets=assets
            )
        )

    return events
