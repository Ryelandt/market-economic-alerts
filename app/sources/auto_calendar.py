import os
import json
import urllib.parse
import urllib.request
from datetime import datetime
from app.models.event import EconomicEvent

BASE_URL = "https://api.stlouisfed.org/fred/releases"


def fetch_events():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("FRED_API_KEY not set")
        return []

    params = {
        "api_key": api_key,
        "file_type": "json",
        "limit": 30
    }

    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print("FRED API error:", e)
        return []

    events = []

    for r in data.get("releases", []):
        name = r["name"]

        # Mapping macro simple
        if "Consumer Price Index" in name:
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
            importance = 3
        elif "Employment Situation" in name:
            assets = ["EURUSD", "XAUUSD", "BTCUSDT"]
            importance = 3
        else:
            continue  # on ignore le bruit

        events.append(
            EconomicEvent(
                name=name,
                datetime=datetime.now(),  # FRED ne donne pas l’heure exacte
                country="US",
                importance=importance,
                forecast=None,
                actual=None,
                affected_assets=assets
            )
        )

    return events
