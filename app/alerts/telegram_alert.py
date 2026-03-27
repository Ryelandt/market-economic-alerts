import os
import json
import urllib.request
from datetime import datetime, timedelta, timezone

# Fuseau horaire robuste (Windows + Linux)
try:
    from zoneinfo import ZoneInfo
    PARIS_TZ = ZoneInfo("Europe/Paris")
except Exception:
    PARIS_TZ = timezone(timedelta(hours=1))

# Anti‑doublon simple par exécution
_SENT_DAILY = False


def send_daily_summary(events):
    global _SENT_DAILY
    if _SENT_DAILY:
        return
    _SENT_DAILY = True

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise RuntimeError("Telegram credentials not set")

    if not events:
        return  # Rien d’important aujourd’hui

    # Tri par heure réelle Paris
    events = sorted(
        events,
        key=lambda e: e.datetime.astimezone(PARIS_TZ)
    )

    lines = []
    for e in events:
        local_time = e.datetime.astimezone(PARIS_TZ)
        lines.append(f"• {local_time.strftime('%H:%M')} — {e.name}")

    message = (
        "📅 AUJOURD’HUI — MACRO IMPORTANT\n\n"
        + "\n".join(lines)
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        response.read()


def send_alert(event, level):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise RuntimeError("Telegram credentials not set")

    now = datetime.now(tz=PARIS_TZ)
    event_time = event.datetime.astimezone(PARIS_TZ)

    # Alerte −30 minutes
    if timedelta(minutes=0) <= (event_time - now) <= timedelta(minutes=30):
        prefix = "⏰ DANS 30 MINUTES\n\n"
    else:
        prefix = ""

    message = (
        f"{prefix}"
        f"🚨 ALERTE {level}\n\n"
        f"📅 {event.name}\n"
        f"⏰ {event_time.strftime('%d/%m %H:%M')}\n\n"
        "🎯 Actifs impactés :\n"
        + "\n".join(f"• {a}" for a in event.affected_assets)
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        response.read()
